from fastapi import APIRouter, status
from typing import List, Optional
from uuid import UUID

from src.entities.user import Role

from ..database.core import DbSession
from . import  models
from . import service
from ..auth.service import CurrentUser, require_any_role

router = APIRouter(
    prefix="/catalogues",
    tags=["Catalogues"],
)


@router.get("/companies/search", response_model=List[models.SearchCompanyResponse])
@require_any_role([Role.CANDIDATE])
def get_resume_companies(db: DbSession, current_user: CurrentUser, query: Optional[str] = None):
    return service.get_resume_companies(current_user, db, query)


@router.get("/institutions/search", response_model=List[models.SearchInstitutionResponse])
@require_any_role([Role.CANDIDATE])
def get_resume_institutions(db: DbSession, current_user: CurrentUser, query: Optional[str] = None):
    return service.get_resume_institutions(current_user, db, query)
