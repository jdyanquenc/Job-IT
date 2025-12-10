from fastapi import APIRouter, status
from typing import List
from uuid import UUID

from ..entities.user import Role
from ..database.core import DbSession
from . import  models
from . import service
from ..auth.service import CurrentUser, require_any_role

router = APIRouter(
    prefix="/companies",
    tags=["Companies"]
)

@router.post("/", response_model=models.CompanyResponse, status_code=status.HTTP_201_CREATED)
def create_company(db: DbSession, company: models.CompanyCreate, current_user: CurrentUser):
    return service.create_company(current_user, db, company)


@router.get("/", response_model=List[models.CompanyResponse])
@require_any_role([Role.CANDIDATE, Role.COMPANY_MANAGER, Role.ADMIN])
def get_companies(db: DbSession, current_user: CurrentUser):
    return service.get_companies(current_user, db)


@router.get("/{company_id}", response_model=models.CompanyResponse)
def get_company(db: DbSession, company_id: UUID, current_user: CurrentUser):
    return service.get_company_by_id(current_user, db, company_id)


@router.put("/{company_id}", response_model=models.CompanyResponse)
def update_company(db: DbSession, company_id: UUID, company_update: models.CompanyCreate, current_user: CurrentUser):
    return service.update_company(current_user, db, company_id, company_update)


@router.put("/{company_id}/complete", response_model=models.CompanyResponse)
def complete_company(db: DbSession, company_id: UUID, current_user: CurrentUser):
    return service.complete_company(current_user, db, company_id)


@router.delete("/{company_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_company(db: DbSession, company_id: UUID, current_user: CurrentUser):
    service.delete_company(current_user, db, company_id)
