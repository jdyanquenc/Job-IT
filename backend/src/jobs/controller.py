from fastapi import APIRouter, status
from typing import List, Optional
from uuid import UUID

from ..entities.user import Role
from ..database.core import DbSession
from . import  models
from . import service
from ..auth.service import CurrentUser, OptionalCurrentUser, require_any_role

router = APIRouter(
    prefix="/jobs",
    tags=["Jobs"]
)

@router.post("/", response_model=models.JobResponse, status_code=status.HTTP_201_CREATED)
@require_any_role([Role.COMPANY_MANAGER])
def create_job(db: DbSession, job: models.JobCreate, current_user: CurrentUser):
    return service.create_job(current_user, db, job)


@router.get("/companies/search", response_model=List[models.JobResponse])
@require_any_role([Role.COMPANY_MANAGER])
def get_company_jobs(db: DbSession, current_user: CurrentUser, query: Optional[str] = None, page: Optional[int] = None):
    return service.get_company_jobs(current_user, db, query, page)


@router.put("/{job_id}", response_model=models.JobDetailResponse)
@require_any_role([Role.COMPANY_MANAGER])
def update_job(db: DbSession, job_id: UUID, todo_update: models.JobUpdate, current_user: CurrentUser):
    return service.update_job(current_user, db, job_id, todo_update)


@router.delete("/{job_id}", status_code=status.HTTP_204_NO_CONTENT)
@require_any_role([Role.COMPANY_MANAGER])
def delete_job(db: DbSession, job_id: UUID, current_user: CurrentUser):
    service.delete_job(current_user, db, job_id)


@router.get("/search", response_model=List[models.JobResponse])
def get_active_jobs(db: DbSession, current_user: OptionalCurrentUser, country_code: str, query: Optional[str] = None, page: Optional[int] = None, page_size: Optional[int] = None, sort_by: Optional[str] = None, sector_ids: Optional[list[UUID]] = None, salary_ranges: Optional[list[int]] = None):
    return service.get_active_jobs(current_user, db, country_code, query, page, page_size, sort_by, sector_ids, salary_ranges)


@router.get("/sectors/counts", response_model=List[models.JobCountBySectorResponse])
def get_job_count_by_sectors(db: DbSession, country_code: str, query: Optional[str] = None, sector_ids: Optional[list[UUID]] = None, salary_ranges: Optional[list[int]] = None):
    return service.get_job_count_by_sectors(db, country_code, query, sector_ids, salary_ranges)


@router.get("/salaries/counts", response_model=List[models.JobCountBySalaryResponse])
def get_job_count_by_salaries(db: DbSession, country_code: str, query: Optional[str] = None, sector_ids: Optional[list[UUID]] = None, salary_ranges: Optional[list[int]] = None):
    return service.get_job_count_by_salaries(db, country_code, query, sector_ids, salary_ranges)


@router.get("/{job_id}", response_model=models.JobDetailResponse)
def get_job(db: DbSession, current_user: OptionalCurrentUser, job_id: UUID):
    return service.get_job_by_id(current_user, db, job_id)


@router.post("/{job_id}/apply", status_code=status.HTTP_201_CREATED)
@require_any_role([Role.CANDIDATE])
def apply_to_job(db: DbSession, current_user: CurrentUser, job_id: UUID):
    service.apply_to_job(current_user, db, job_id)


@router.get("/{job_id}/applicants", response_model=List[models.JobApplicantResponse])
@require_any_role([Role.COMPANY_MANAGER])
def get_job_applicants(db: DbSession, current_user: CurrentUser, job_id: UUID, query: Optional[str] = None, page: Optional[int] = None):
    return service.get_job_applicants(current_user, db, job_id, query, page)


@router.get("/applications/", response_model=List[models.JobApplicationResponse])
@require_any_role([Role.CANDIDATE])
def get_job_applications(db: DbSession, current_user: CurrentUser, query: Optional[str] = None, page: Optional[int] = None):
    return service.get_job_applications(current_user, db, query, page)


@router.get("/recommendations/", response_model=List[models.JobApplicationResponse])
@require_any_role([Role.CANDIDATE])
def get_job_recommendations(db: DbSession, current_user: CurrentUser, query: Optional[str] = None, page: Optional[int] = None):
    return service.get_job_recommendations(current_user, db, query, page)
