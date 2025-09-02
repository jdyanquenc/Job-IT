from datetime import datetime, timezone
from uuid import uuid4, UUID

from sqlalchemy import text
from sqlalchemy.orm import Session
from fastapi import HTTPException

from . import models
from src.auth.models import TokenData
from src.entities.job import EmploymentType, JobEntry, JobDetail
from src.entities.company import Company
from src.exceptions import JobCreationError, JobNotFoundError
import logging

def create_job(current_user: TokenData, db: Session, job: models.JobCreate) -> models.JobResponse:
    try:
        job_uuid = uuid4()
        new_job_entry = model_from_dto(job, JobEntry)
        new_job_detail = model_from_dto(job, JobDetail)
        new_job_entry.user_id = current_user.get_uuid()
        new_job_entry.company_id = current_user.get_company_uuid()
        new_job_entry.id = job_uuid
        new_job_detail.id = job_uuid
        new_job_entry.job_short_description = new_job_detail.job_description[:100]
        db.add(new_job_entry)
        db.add(new_job_detail)
        db.commit()
        db.refresh(new_job_entry)
        company = db.query(Company).filter(Company.id == new_job_entry.company_id).first()
        logging.info(f"Created new job for user: {current_user.get_uuid()}")
        
        return models.JobResponse(
            id = new_job_entry.id,
            job_title = new_job_entry.job_title,
            job_short_description = new_job_entry.job_short_description,
            remote = new_job_entry.remote,
            employment_type = new_job_entry.employment_type,
            skills_required = new_job_entry.skills_required,
            salary_range = new_job_entry.salary_range,
            expires_at = new_job_entry.expires_at,
            created_at = new_job_entry.created_at,
            company = models.CompanyBasicInfo(
                name = company.name,
                location = company.location,
                country_code = company.country.iso_code,
                image_url = company.image_url
            )
        )

    except Exception as e:
        logging.error(f"Failed to create job for user {current_user.get_uuid()}. Error: {str(e)}")
        raise JobCreationError(str(e))


def get_active_jobs(current_user: TokenData, db: Session, query: str, page: int = 1, page_size: int = 20) -> list[models.JobResponse]:

    stmt = text("""
        SELECT j.id, j.job_title, j.job_short_description, j.remote, j.employment_type, j.skills_required, j.salary_range, j.expires_at, j.created_at, c.name AS company_name, c.location AS company_location, co.iso_code AS company_country_code, c.image_url AS company_image_url
        FROM job_entry j
        JOIN company c ON c.id = j.company_id
        JOIN country co ON co.id = c.country_id
        WHERE is_active = true
        AND search_vector @@ plainto_tsquery('english', :query)
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
            skills_required = skills_required,
            salary_range = salary_range,
            expires_at = expires_at,
            created_at = created_at,
            company = models.CompanyBasicInfo(
                name = company_name,
                location = company_location,
                country_code = company_country_code,
                image_url = company_image_url
            )
        )
        for id, job_title, job_short_description, remote, employment_type, skills_required, salary_range, expires_at, created_at, company_name, company_location, company_country_code, company_image_url in results
    ]

    logging.info(f"Retrieved {len(jobs)} jobs for user: {current_user.get_uuid()}")
    return jobs


def get_job_by_id(current_user: TokenData, db: Session, job_id: UUID) -> models.JobDetailResponse:
    job = db.query(JobEntry).filter(JobEntry.id == job_id).first()
    if not job:
        logging.warning(f"Job {job_id} not found for user {current_user.get_uuid()}")
        raise JobNotFoundError(job_id)
    
    company = db.query(Company).filter(Company.id == job.company_id).first()
   
    logging.info(f"Retrieved Job {job_id} for user {current_user.get_uuid()}")
    return models.JobDetailResponse(
        id = job.id,
        job_title = job.job_title,
        job_description = job.detail.job_description,
        experience = job.detail.experience,
        qualifications = job.detail.qualifications,
        responsibilities = job.detail.responsibilities,
        benefits = job.detail.benefits,
        remote = job.remote,
        employment_type = job.employment_type,
        skills_required = job.skills_required,
        salary_range = job.salary_range,
        created_at = job.created_at,
        updated_at = job.updated_at,
        expires_at = job.expires_at,
        is_active = job.is_active,
        company = models.CompanyBasicInfo(
            name = company.name,
            location = company.location,
            country_code = company.country.iso_code,
            image_url = company.image_url
        )
    )


def update_job(current_user: TokenData, db: Session, job_id: UUID, job_update: models.JobUpdate) -> models.JobDetailResponse:
    # TODO Check user permission to update job
    job_data = job_update.model_dump(exclude_unset=True)
    db.query(JobEntry).filter(JobEntry.id == job_id).update(job_data)
    db.commit()
    logging.info(f"Successfully updated todo {job_id} for user {current_user.get_uuid()}")
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