from datetime import datetime, timezone
from uuid import uuid4, UUID

from sqlalchemy import text
from sqlalchemy.orm import Session
from fastapi import HTTPException

from . import models
from src.auth.models import TokenData
from src.entities.job import  JobEntry, JobDetail
from src.entities.company import Company
from src.entities.country import Country
from src.exceptions import JobCreationError, JobNotFoundError
import logging

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
        new_job_entry.id = job_uuid
        new_job_detail.id = job_uuid
        new_job_entry.job_short_description = new_job_detail.job_description[:100]
        db.add(new_job_entry)
        db.add(new_job_detail)
        db.commit()
        db.refresh(new_job_entry)
        
        logging.info(f"Created new job for user: {current_user.get_uuid()}")
        
        return models.JobResponse(
            id = new_job_entry.id,
            job_title = new_job_entry.job_title,
            job_short_description = new_job_entry.job_short_description,
            remote = new_job_entry.remote,
            employment_type = new_job_entry.employment_type,
            tags = new_job_entry.tags,
            salary_range = new_job_entry.salary_range,
            expires_at = new_job_entry.expires_at,
            created_at = new_job_entry.created_at,
            company = models.CompanyBasicInfo(
                name = company.name,
                image_url = company.image_url,
                location = new_job_entry.location,
                country_code = country.iso_code
            )
        )

    except Exception as e:
        logging.error(f"Failed to create job for user {current_user.get_uuid()}. Error: {str(e)}")
        raise JobCreationError(str(e))


def get_active_jobs(current_user: TokenData, db: Session, query: str, page: int = 1, page_size: int = 20) -> list[models.JobResponse]:

    stmt = text("""
        SELECT j.id, j.job_title, j.job_short_description, j.remote, j.employment_type, j.tags, j.salary_range, j.expires_at, j.created_at, c.name AS company_name, j.location, co.iso_code AS country_code, c.image_url
        FROM job_entry j
        JOIN company c ON c.id = j.company_id
        JOIN country co ON co.id = j.country_id
        WHERE is_active = true
        AND (:query = '' OR search_vector @@ plainto_tsquery('english', :query))
        ORDER BY ts_rank_cd(search_vector, plainto_tsquery('english', :query)) DESC
        LIMIT :limit OFFSET :offset
    """)
    results = db.execute(stmt, {
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
            tags = tags,
            salary_range = salary_range,
            expires_at = expires_at,
            created_at = created_at,
            location = location,
            country_code = country_code,
            company_name = company_name,
            company_image_url = image_url or ""
        )
        for id, job_title, job_short_description, remote, employment_type, tags, salary_range, expires_at, created_at, company_name, location, country_code, image_url in results
    ]

    logging.info(f"Retrieved {len(jobs)} jobs for user: {current_user.get_uuid()}")
    return jobs


def get_job_by_id(current_user: TokenData, db: Session, job_id: UUID) -> models.JobDetailResponse:
    job = db.query(JobEntry).filter(JobEntry.id == job_id).first()
    if not job:
        logging.warning(f"Job {job_id} not found for user {current_user.get_uuid()}")
        raise JobNotFoundError(job_id)
    
    company = db.query(Company).filter(Company.id == job.company_id).first()
    country = db.query(Country).filter(Country.id == job.country_id).first()
   
    logging.info(f"Retrieved Job {job_id} for user {current_user.get_uuid()}")
    return models.JobDetailResponse(
        id = job.id,
        job_title = job.job_title,
        job_description = job.detail.job_description,
        responsibilities = job.detail.responsibilities,
        skills = job.detail.skills,
        benefits = job.detail.benefits,
        experience = job.detail.experience,
        employment_type = job.employment_type,
        remote = job.remote,
        salary_range = job.salary_range,
        tags = job.tags or [],
        created_at = job.created_at,
        updated_at = job.updated_at,
        expires_at = job.expires_at,
        is_active = job.is_active,
        location = job.location,
        country_code = country.iso_code,
        company_name = company.name,
        company_image_url = company.image_url
    )


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
    job_entry.salary_range = job_update.salary_range
    job_entry.tags = job_update.tags
    job_entry.expires_at = job_update.expires_at
    job_entry.updated_at = datetime.now(timezone.utc)
    job_entry.country_id = country.id
 
    job_detail.job_description = job_update.job_description
    job_detail.responsibilities = job_update.responsibilities
    job_detail.skills = job_update.skills
    job_detail.benefits = job_update.benefits
    job_detail.experience = job_update.experience

    db.commit()
    logging.info(f"Successfully updated job {job_id} for user {current_user.get_uuid()}")
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


def model_from_dto(dto, model_cls):
    valid_fields = {c.name for c in model_cls.__table__.columns}
    data = {k: v for k, v in dto.dict().items() if k in valid_fields}
    return model_cls(**data)