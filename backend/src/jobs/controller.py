from fastapi import APIRouter, Depends, Query, status
from typing import List, Optional, Union
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
def get_active_jobs(db: DbSession, current_user: OptionalCurrentUser, filters: models.JobFilters = Depends(models.get_job_filters)):
    return service.get_active_jobs(current_user, db, filters)


@router.get("/counts", response_model=List[models.JobCountsResponse])
def get_active_jobs_counts(db: DbSession, filters: models.JobFilters = Depends(models.get_job_filters)):
    return service.get_active_jobs_counts(db, filters)


@router.get("/{job_id}", response_model=models.JobDetailResponse)
def get_job(db: DbSession, current_user: OptionalCurrentUser, job_id: UUID):
    return service.get_job_by_id(current_user, db, job_id)

@router.get("/{job_id}/related", response_model=List[models.JobResponse])
async def get_related_jobs(db: DbSession, current_user: OptionalCurrentUser, job_id: UUID):
    return await service.get_related_jobs(current_user, db, job_id)


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

