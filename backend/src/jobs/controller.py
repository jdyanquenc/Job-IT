from fastapi import APIRouter, status
from typing import List, Optional
from uuid import UUID

from ..entities.user import Role
from ..database.core import DbSession
from . import  models
from . import service
from ..auth.service import CurrentUser, require_any_role

router = APIRouter(
    prefix="/jobs",
    tags=["Jobs"]
)

@router.post("/", response_model=models.JobResponse, status_code=status.HTTP_201_CREATED)
@require_any_role([Role.COMPANY_MANAGER, Role.ADMIN])
def create_job(db: DbSession, job: models.JobCreate, current_user: CurrentUser):
    return service.create_job(current_user, db, job)


@router.get("/search", response_model=List[models.JobResponse])
def get_active_jobs(db: DbSession, current_user: CurrentUser, query: Optional[str] = None, page: Optional[int] = None):
    return service.get_active_jobs(current_user, db, query, page)


@router.get("/{job_id}", response_model=models.JobDetailResponse)
def get_job(db: DbSession, job_id: UUID, current_user: CurrentUser):
    return service.get_job_by_id(current_user, db, job_id)


@router.put("/{job_id}", response_model=models.JobDetailResponse)
def update_job(db: DbSession, job_id: UUID, todo_update: models.JobUpdate, current_user: CurrentUser):
    return service.update_job(current_user, db, job_id, todo_update)


@router.delete("/{job_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_job(db: DbSession, job_id: UUID, current_user: CurrentUser):
    service.delete_job(current_user, db, job_id)
