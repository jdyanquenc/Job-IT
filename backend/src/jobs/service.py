from datetime import datetime, timezone
from uuid import uuid4, UUID

import os
import httpx
from sqlalchemy import text
from sqlalchemy.orm import Session

from src.auth.service import OptionalCurrentUser
from src.entities.company_user import CompanyUser
from src.entities.currency import Currency
from src.entities.job_application import JobApplication, JobApplicationStatus
from src.entities.user import User
from src.messaging.rabbitmq_service import RabbitMQService

from . import models
from src.auth.models import TokenData
from src.entities.job import  JobEntry, JobDetail
from src.entities.company import Company
from src.entities.country import Country
from src.exceptions import JobAccessError, JobAlreadyAppliedError, JobCreationError, JobNotFoundError, JobsRelatedError, UserNotFoundError
from dotenv import load_dotenv
import logging


load_dotenv()

RECOMMENDATION_ENGINE_URL = os.getenv("RECOMMENDATION_ENGINE_URL", "http://localhost:5000")

def create_job(current_user: TokenData, db: Session, job: models.JobCreate) -> models.JobResponse:
    try:
        country = db.query(Country).filter(Country.iso_code == job.country_code).first()
        company = db.query(Company).filter(Company.id == current_user.get_company_uuid()).first()
        

        job_uuid = uuid4()
        new_job_entry = model_from_dto(job, JobEntry)
        new_job_detail = model_from_dto(job, JobDetail)
        new_job_entry.user_id = current_user.get_uuid()
        new_job_entry.company_id = company.id
        new_job_entry.country_id = country.id
        new_job_entry.currency_id = country.currency_id
        new_job_entry.id = job_uuid
        new_job_detail.id = job_uuid
        new_job_entry.job_short_description = new_job_detail.job_description[:100]
        db.add(new_job_entry)
        db.add(new_job_detail)
        db.commit()
        db.refresh(new_job_entry)
        
        logging.info(f"Created new job for user: {current_user.get_uuid()}")
        send_job_changed_event(new_job_entry, "job.created")

        return models.JobResponse(
            id = new_job_entry.id,
            job_title = new_job_entry.job_title,
            job_short_description = new_job_entry.job_short_description,
            remote = new_job_entry.remote,
            employment_type = new_job_entry.employment_type,
            tags = new_job_entry.tags,
            salary_min = new_job_entry.salary_min,
            salary_max = new_job_entry.salary_max,
            experience_min_years = new_job_entry.experience_min_years,
            currency_code = country.currency.code if country.currency else None,
            created_at = new_job_entry.created_at,
            expires_at = new_job_entry.expires_at,
            company_name = company.name,
            company_image_url = company.image_url or "",
            has_applied = False
        )

    except Exception as e:
        logging.error(f"Failed to create job for user {current_user.get_uuid()}. Error: {str(e)}")
        raise JobCreationError(str(e))


def get_company_jobs(current_user: TokenData, db: Session, query: str, page: int = 1, page_size: int = 20) -> list[models.JobResponse]:
    stmt = text("""
        SELECT j.id, j.job_title, j.job_short_description, j.remote, j.employment_type, j.tags, j.salary_min, j.salary_max, j.experience_min_years, cu.code, j.expires_at, j.created_at, c.name AS company_name, j.location, co.iso_code AS country_code, c.image_url
        FROM job_entry j
        JOIN company c ON c.id = j.company_id
        JOIN country co ON co.id = j.country_id
        JOIN currency cu ON cu.id = j.currency_id
        WHERE j.company_id = :company_id
        AND (:query = '' OR search_vector @@ plainto_tsquery('english', :query))
        ORDER BY ts_rank_cd(search_vector, plainto_tsquery('english', :query)) DESC
        LIMIT :limit OFFSET :offset
    """)
    results = db.execute(stmt, {
        "company_id": current_user.get_company_uuid(),
        "query": query,
        "limit": page_size,
        "offset": (page - 1) * page_size
    }).fetchall()

    # Convert to list of Pydantic models
    jobs = [
        models.JobResponse(
            id = id,
            job_title = job_title,
            job_short_description = job_short_description,
            remote = remote,
            employment_type = employment_type,
            tags = tags or [],
            salary_min = salary_min,
            salary_max = salary_max,
            experience_min_years = experience_min_years,
            currency_code = currency_code,
            expires_at = expires_at,
            created_at = created_at,
            location = location,
            country_code = country_code,
            company_name = company_name,
            company_image_url = image_url or "",
            has_applied = False  # Company jobs view does not track applications
        )
        for id, job_title, job_short_description, remote, employment_type, tags, salary_min, salary_max, experience_min_years, currency_code, expires_at, created_at, company_name, location, country_code, image_url in results
    ]

    logging.info(f"Retrieved {len(jobs)} jobs for company: {current_user.get_company_uuid()}")
    return jobs


def get_active_jobs(current_user: OptionalCurrentUser, db: Session, filters: models.JobFilters) -> list[models.JobResponse]:

    if filters.sort_by not in ['relevance', 'date', 'salary']:
        filters.sort_by = 'relevance'

    if filters.sector_ids:
        sector_filter = "AND c.sector_id = ANY(:sector_ids)"
    else:
        sector_filter = ""

    if filters.salary_ranges:
        salary_filter = "AND EXISTS (SELECT 1 FROM job_salary js WHERE (j.salary_min >= js.min_salary AND j.salary_max < js.max_salary) AND js.id = ANY(:salary_ranges))"
    else:
        salary_filter = ""

    order_by_clause = {
        'relevance': "ORDER BY ts_rank_cd(search_vector, plainto_tsquery('english', :query)) DESC",
        'date': "ORDER BY j.created_at DESC",
        'salary': "ORDER BY j.salary_min DESC"
    }.get(filters.sort_by)

    stmt = text(f"""
        SELECT j.id, j.job_title, j.job_short_description, j.remote, j.employment_type, j.tags, (j.salary_min / cu.divisor), (j.salary_max / cu.divisor), j.experience_min_years, cu.code, j.expires_at, j.created_at, c.name AS company_name, j.location, co.iso_code AS country_code, c.image_url, (ja.job_id IS NOT NULL) AS has_applied
        FROM job_entry j
        JOIN company c ON c.id = j.company_id
        JOIN country co ON co.id = j.country_id
        LEFT JOIN currency cu ON cu.id = j.currency_id
        LEFT JOIN job_application ja ON ja.job_id = j.id AND ja.user_id = :user_id
        WHERE is_active = true
        AND co.iso_code = :country_code
        AND (:query = '' OR search_vector @@ plainto_tsquery('english', :query))
        {sector_filter}
        {salary_filter}
        {order_by_clause}
        LIMIT :limit OFFSET :offset
    """)
    results = db.execute(stmt, {
        "country_code": filters.country_code,
        "query": filters.query,
        "user_id": current_user.get_uuid() if current_user else None,
        "limit": filters.page_size,
        "offset": (filters.page - 1) * filters.page_size,
        "sector_ids": filters.sector_ids,
        "salary_ranges": filters.salary_ranges
    }).fetchall()

    logging.info(f"User {current_user.get_uuid() if current_user else None} retrieved active jobs with query '{filters.query}' on page {filters.page}")

    # Convert to list of Pydantic models
    jobs = [
        models.JobResponse(
            id = id,
            job_title = job_title,
            job_short_description = job_short_description,
            remote = remote,
            employment_type = employment_type,
            tags = tags or [],
            salary_min = salary_min,
            salary_max = salary_max,
            experience_min_years = experience_min_years,
            currency_code = currency_code,
            expires_at = expires_at,
            created_at = created_at,
            location = location,
            country_code = country_code,
            company_name = company_name,
            company_image_url = image_url or "",
            has_applied = has_applied
        )
        for id, job_title, job_short_description, remote, employment_type, tags, salary_min, salary_max, experience_min_years, currency_code, expires_at, created_at, company_name, location, country_code, image_url, has_applied in results
    ]

    logging.info(f"Retrieved {len(jobs)} jobs")
    return jobs


def get_active_jobs_counts(db: Session, filters: models.JobFilters) -> list[models.JobCountsResponse]:

    if filters.sector_ids:
        sector_filter = "AND c.sector_id = ANY(:sector_ids)"
    else:
        sector_filter = ""

    if filters.salary_ranges:
        salary_filter = "AND EXISTS (SELECT 1 FROM job_salary js WHERE (j.salary_min >= js.min_salary AND j.salary_max < js.max_salary) AND js.id = ANY(:salary_ranges))"
    else:
        salary_filter = ""

    stmt = text(f"""
        WITH job_counts AS (
            SELECT c.sector_id, js.id, count(1) AS job_count
            FROM job_entry j
            JOIN company c ON c.id = j.company_id
            JOIN country co ON co.id = j.country_id
            LEFT JOIN job_salary js ON COALESCE(j.salary_min, 0) >= js.min_salary AND COALESCE(j.salary_max, 0) < js.max_salary 
            WHERE is_active = true
            AND co.iso_code = :country_code
            AND (:query = '' OR search_vector @@ plainto_tsquery('english', :query))
            {sector_filter}
            {salary_filter}
            GROUP BY c.sector_id, js.id
        )
        SELECT 'SECTOR' as type, s.id::text as id, s."name" as name, SUM(COALESCE(job_count, 0)) as job_count
        FROM sector s
        LEFT JOIN job_counts j ON j.sector_id = s.id 
        GROUP BY s.id

        UNION

        SELECT 'SALARY', js.id::text, js.display_name, SUM(COALESCE(job_count, 0))
        FROM job_salary js
        LEFT JOIN job_counts j ON j.id = js.id
        GROUP BY js.id

        UNION

        SELECT 'TOTAL', '0', 'Total', SUM(COALESCE(job_count, 0))
        FROM job_counts j
        ORDER BY 1, 2
    """)
    results = db.execute(stmt, {
        "country_code": filters.country_code,
        "query": filters.query,
        "sector_ids": filters.sector_ids,
        "salary_ranges": filters.salary_ranges
    }).fetchall()

    sectors = [
        models.JobCountsResponse(
            type = type,
            id = id,
            name = name,
            count = job_count
        )
        for type, id, name, job_count in results
    ]

    logging.info(f"Retrieved {len(sectors)} job sectors for country {filters.country_code} with query '{filters.query}'")
    return sectors


def get_job_by_id(current_user: OptionalCurrentUser, db: Session, job_id: UUID) -> models.JobDetailResponse:
    job = db.query(JobEntry).filter(JobEntry.id == job_id).first()
    if not job:
        logging.warning(f"Job {job_id} not found")
        raise JobNotFoundError(job_id)
    
    company = db.query(Company).filter(Company.id == job.company_id).first()
    country = db.query(Country).filter(Country.id == job.country_id).first()
    currency = db.query(Currency).filter(Currency.id == job.currency_id).first()
    has_applied = db.query(JobApplication).filter(JobApplication.job_id == job_id).filter(JobApplication.user_id == current_user.get_uuid() if current_user else None).first() is not None

    logging.info(f"Retrieved Job with ID {job_id}")
    return models.JobDetailResponse(
        id = job.id,
        job_title = job.job_title,
        job_description = job.detail.job_description,
        responsibilities = job.detail.responsibilities,
        skills = job.detail.skills,
        benefits = job.detail.benefits,
        employment_type = job.employment_type,
        remote = job.remote,
        salary_min = job.salary_min,
        salary_max = job.salary_max,
        currency_code = currency.code if currency else None,
        experience_min_years = job.experience_min_years,
        tags = job.tags or [],
        created_at = job.created_at,
        updated_at = job.updated_at,
        expires_at = job.expires_at,
        is_active = job.is_active,
        location = job.location,
        country_code = country.iso_code,
        company_name = company.name,
        company_image_url = company.image_url or "",
        has_applied = has_applied
    )


async def get_related_jobs(current_user: OptionalCurrentUser, db: Session, job_id: UUID) -> list[models.JobResponse]:
    # Invoke the recommendation engine via HTTP to get related job IDs
    external_url = RECOMMENDATION_ENGINE_URL + f"/jobs/{job_id}/related"

    logging.info(f"Trying to fetch related jobs for job ID {job_id} from {external_url}")

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(external_url)
            response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
            data = response.json()

        # load related jobs details from database

        related_job_ids = [str(item[0]) for item in data]
        jobs = db.query(JobEntry).filter(JobEntry.id.in_(related_job_ids)).all()
        job_responses = []
        for job in jobs:
            company = db.query(Company).filter(Company.id == job.company_id).first()
            country = db.query(Country).filter(Country.id == job.country_id).first()
            currency = db.query(Currency).filter(Currency.id == job.currency_id).first()
            has_applied = db.query(JobApplication).filter(JobApplication.job_id == job.id).filter(JobApplication.user_id == current_user.get_uuid() if current_user else None).first() is not None

            job_responses.append(
                models.JobResponse(
                    id = job.id,
                    job_title = job.job_title,
                    job_short_description = job.job_short_description,
                    remote = job.remote,
                    employment_type = job.employment_type,
                    tags = job.tags or [],
                    salary_min = job.salary_min,
                    salary_max = job.salary_max,
                    experience_min_years = job.experience_min_years,
                    currency_code = currency.code if currency else None,
                    expires_at = job.expires_at,
                    created_at = job.created_at,
                    location = job.location,
                    country_code = country.iso_code,
                    company_name = company.name,
                    company_image_url = company.image_url or "",
                    has_applied = has_applied
                )
            )
        return job_responses

    except Exception as e:
        logging.error(f"Unexpected error while fetching related jobs for job ID {job_id}: {str(e)}")
        raise JobsRelatedError(job_id=job_id, detail=f"An unexpected error occurred: {e}")
    


def update_job(current_user: TokenData, db: Session, job_id: UUID, job_update: models.JobUpdate) -> models.JobDetailResponse:
    # TODO Check user permission to update job
    country = db.query(Country).filter(Country.iso_code == job_update.country_code).first()
    job_entry = db.query(JobEntry).filter(JobEntry.id == job_id).first()
    job_detail = db.query(JobDetail).filter(JobDetail.id == job_id).first()

    if not job_entry or not job_detail:
        logging.warning(f"Job {job_id} not found for user {current_user.get_uuid()}")
        raise JobNotFoundError(job_id)

    job_entry.title = job_update.job_title
    job_entry.job_short_description = job_update.job_description[:100]
    job_entry.remote = job_update.remote
    job_entry.location = job_update.location
    job_entry.employment_type = job_update.employment_type
    job_entry.salary_min = job_update.salary_min
    job_entry.salary_max = job_update.salary_max
    job_entry.experience_min_years = job_update.experience_min_years
    job_entry.tags = job_update.tags
    job_entry.expires_at = job_update.expires_at
    job_entry.updated_at = datetime.now(timezone.utc)
    job_entry.country_id = country.id
    job_entry.currency_id = country.currency_id
 
    job_detail.job_description = job_update.job_description
    job_detail.responsibilities = job_update.responsibilities
    job_detail.skills = job_update.skills
    job_detail.benefits = job_update.benefits
    job_detail.experience = job_update.experience

    db.commit()
    logging.info(f"Successfully updated job {job_id} for user {current_user.get_uuid()}")

    send_job_changed_event(job_entry, "job.updated")
    return get_job_by_id(current_user, db, job_id)


def delete_job(current_user: TokenData, db: Session, job_id: UUID) -> None:
    # TODO Check user permission to delete job
    job = db.query(JobEntry).filter(JobEntry.id == job_id).first()
    if not job:
        logging.warning(f"Job {job_id} not found for user {current_user.get_uuid()}")
        raise JobNotFoundError(job_id)
    
    db.delete(job)
    db.commit()
    logging.info(f"Job {job_id} deleted by user {current_user.get_uuid()}")


def apply_to_job(current_user: TokenData, db: Session, job_id: UUID) -> None:
    job = db.query(JobEntry).filter(JobEntry.id == job_id, JobEntry.is_active == True).first()
    if not job:
        logging.warning(f"Job {job_id} not found or inactive for user {current_user.get_uuid()}")
        raise JobNotFoundError(job_id)

    existing_application = db.query(JobApplication).filter(JobApplication.job_id == job_id, JobApplication.user_id == current_user.get_uuid()).first()
    if existing_application:
        logging.warning(f"User {current_user.get_uuid()} has already applied to job {job_id}")
        raise JobAlreadyAppliedError(job_id)

    new_application = JobApplication(
        job_id = job_id,
        user_id = current_user.get_uuid(),
        status = JobApplicationStatus.Applied,
        applied_at = datetime.now(timezone.utc)
    )
    db.add(new_application)
    db.commit()
    logging.info(f"User {current_user.get_uuid()} applied to job {job_id}")
    return
    

def get_job_applicants(current_user: TokenData, db: Session, job_id: UUID, query: str, page: int = 1, page_size: int = 20) -> list[models.JobApplicantResponse]:
    # Check user permission to view job applications
    job = db.query(JobEntry).filter(JobEntry.id == job_id).first()
    company_user = db.query(CompanyUser).filter(CompanyUser.user_id == current_user.get_uuid()).first()

    if company_user.company_id != job.company_id:
        logging.warning(f"User {current_user.get_uuid()} does not have permission to view applications for job {job_id}")
        raise JobAccessError(job_id)

    stmt = text("""
        SELECT ja.job_id, ja.user_id, u.first_name, u.last_name, up.title, up.description, up.skills, up.location, ja.status, ja.applied_at
        FROM job_application ja
        JOIN users u ON u.id = ja.user_id
        JOIN user_profile up ON up.id = u.id
        WHERE ja.job_id = :job_id
        AND (:query = '' OR (u.first_name || ' ' || u.last_name || ' ' || up.title || ' ' || up.description || ' ' || up.skills) ILIKE '%' || :query || '%')
        ORDER BY ja.applied_at DESC
        LIMIT :limit OFFSET :offset
    """)
    results = db.execute(stmt, {
        "query": query,
        "limit": page_size,
        "offset": (page - 1) * page_size,
        "job_id": job_id
    }).fetchall()

    applications = [
        models.JobApplicantResponse(
            job_id = job_id,
            user_id = user_id,
            first_name = first_name,
            last_name = last_name,
            title = title,
            description = description,
            skills = skills,
            location = location,
            status = status,
            applied_at = applied_at
        )
        for job_id, user_id, first_name, last_name, title, description, skills, location, status, applied_at in results
    ]

    return applications



def get_job_applications(current_user: TokenData, db: Session, query: str, page: int = 1, page_size: int = 20) -> list[models.JobApplicantResponse]:
    user = db.query(User).filter(User.id == current_user.get_uuid()).first()
    if not user:
        logging.warning(f"User {current_user.get_uuid()} not found")
        raise UserNotFoundError(current_user.get_uuid())

    stmt = text("""
        SELECT j.id, j.job_title, j.job_short_description, j.remote, j.employment_type, j.tags, (j.salary_min / cu.divisor), (j.salary_max / cu.divisor), cu.code, j.expires_at, j.created_at, c.name AS company_name, j.location, co.iso_code AS country_code, c.image_url, (ja.job_id IS NOT NULL) AS has_applied
        FROM job_entry j
        JOIN company c ON c.id = j.company_id
        JOIN country co ON co.id = j.country_id
        JOIN currency cu ON cu.id = j.currency_id
        JOIN job_application ja ON ja.job_id = j.id AND ja.user_id = :user_id
        WHERE j.is_active = true
        AND ja.user_id = :user_id
        AND (:query = '' OR search_vector @@ plainto_tsquery('english', :query))
        ORDER BY ts_rank_cd(search_vector, plainto_tsquery('english', :query)) DESC
        LIMIT :limit OFFSET :offset
    """)
    results = db.execute(stmt, {
        "query": query,
        "limit": page_size,
        "offset": (page - 1) * page_size,
        "user_id": current_user.get_uuid()
    }).fetchall()

    applications = [
        models.JobApplicationResponse(
            id = id,
            job_title = job_title,
            job_short_description = job_short_description,
            remote = remote,
            employment_type = employment_type,
            tags = tags,
            salary_min = salary_min,
            salary_max = salary_max,
            currency_code = currency_code,
            expires_at = expires_at,
            created_at = created_at,
            location = location,
            country_code = country_code,
            company_name = company_name,
            company_image_url = image_url or "",
            has_applied = has_applied
        )
        for id, job_title, job_short_description, remote, employment_type, tags, salary_min, salary_max, currency_code, expires_at, created_at, company_name, location, country_code, image_url, has_applied in results
    ]

    return applications


def get_job_recommendations(current_user: TokenData, db: Session, query: str, page: int = 1, page_size: int = 20) -> list[models.JobRecommendationResponse]:
    user = db.query(User).filter(User.id == current_user.get_uuid()).first()
    if not user:
        logging.warning(f"User {current_user.get_uuid()} not found")
        raise UserNotFoundError(current_user.get_uuid())

    stmt = text("""
        SELECT j.id, j.job_title, j.job_short_description, j.remote, j.employment_type, j.tags, (j.salary_min / cu.divisor), (j.salary_max / cu.divisor), cu.code, j.expires_at, j.created_at, c.name AS company_name, j.location, co.iso_code AS country_code, c.image_url, (ja.job_id IS NOT NULL) AS has_applied
        FROM job_entry j
        JOIN company c ON c.id = j.company_id
        JOIN country co ON co.id = j.country_id
        LEFT JOIN currency cu ON cu.id = j.currency_id
        JOIN job_recommendation jr ON jr.job_id = j.id AND jr.user_id = :user_id
        LEFT JOIN job_application ja ON ja.job_id = j.id AND ja.user_id = :user_id
        WHERE j.is_active = true
        AND (:query = '' OR search_vector @@ plainto_tsquery('english', :query))
        ORDER BY jr.similarity_score DESC
        LIMIT :limit OFFSET :offset
    """)
    results = db.execute(stmt, {
        "query": query,
        "limit": page_size,
        "offset": (page - 1) * page_size,
        "user_id": current_user.get_uuid()
    }).fetchall()

    recommendations = [
        models.JobRecommendationResponse(
            id = id,
            job_title = job_title,
            job_short_description = job_short_description,
            remote = remote,
            employment_type = employment_type,
            tags = tags or [],
            salary_min = salary_min,
            salary_max = salary_max,
            currency_code = currency_code,
            expires_at = expires_at,
            created_at = created_at,
            location = location,
            country_code = country_code,
            company_name = company_name,
            company_image_url = image_url or "",
            has_applied = has_applied
        )
        for id, job_title, job_short_description, remote, employment_type, tags, salary_min, salary_max, currency_code, expires_at, created_at, company_name, location, country_code, image_url, has_applied in results
    ]

    return recommendations



def model_from_dto(dto, model_cls):
    valid_fields = {c.name for c in model_cls.__table__.columns}
    data = {k: v for k, v in dto.dict().items() if k in valid_fields}
    return model_cls(**data)


def job_to_dict(job_entry):
    return {
        "job_id": str(job_entry.id),
        "job_expiration": job_entry.expires_at.isoformat() if job_entry.expires_at else None,
        "job_detail": "{} {} {} {}".format(
            job_entry.job_title,
            job_entry.detail.job_description,
            job_entry.detail.responsibilities,
            job_entry.detail.skills
        )
    }

def send_job_changed_event(job_entry, queue):
    data = job_to_dict(job_entry)
    try:
        RabbitMQService.publish_event_async(queue, data)
        
    except Exception as e:
        logging.error(f"Failed to send {queue} event for job {job_entry.id}. Error: {str(e)}")