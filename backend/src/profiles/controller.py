from fastapi import APIRouter
from typing import List
from uuid import UUID

from src.entities.user import Role

from ..database.core import DbSession
from . import  models
from . import service
from ..auth.service import CurrentUser, require_any_role

router = APIRouter(
    prefix="/profiles",
    tags=["Profiles"]
)

@router.get("/{profile_id}", response_model=models.ProfileResponse)
@require_any_role([Role.CANDIDATE, Role.COMPANY_MANAGER, Role.ADMIN])
def get_profile_data(db: DbSession, profile_id: UUID, current_user: CurrentUser):
    return service.get_profile(current_user, db, profile_id)

@router.put("/{profile_id}", response_model=models.ProfileResponse)
@require_any_role([Role.CANDIDATE])
def update_profile(db: DbSession, profile_id: UUID, profile_update: models.ProfileUpdate, current_user: CurrentUser):
    return service.update_profile(current_user, db, profile_id, profile_update)

@router.post("/{profile_id}/work-experiences", response_model=models.WorkExperienceResponse)
@require_any_role([Role.CANDIDATE])
def add_working_experience(db: DbSession, profile_id: UUID, work_experience: models.WorkExperienceRequest, current_user: CurrentUser):
    return service.add_working_experience(current_user, db, profile_id, work_experience)

@router.put("/{profile_id}/work-experiences/{experience_id}", response_model=models.WorkExperienceResponse)
@require_any_role([Role.CANDIDATE])
def update_working_experience(db: DbSession, profile_id: UUID, experience_id: UUID, work_experience: models.WorkExperienceRequest, current_user: CurrentUser):
    return service.update_working_experience(current_user, db, profile_id, experience_id, work_experience)

@router.delete("/{profile_id}/work-experiences/{experience_id}", status_code=204)
@require_any_role([Role.CANDIDATE])
def delete_working_experience(db: DbSession, profile_id: UUID, experience_id: UUID, current_user: CurrentUser):
    return service.delete_working_experience(current_user, db, profile_id, experience_id)


@router.post("/{profile_id}/educations", response_model=models.EducationResponse)
@require_any_role([Role.CANDIDATE])
def add_education(db: DbSession, profile_id: UUID, education: models.EducationRequest, current_user: CurrentUser):
    return service.add_education(current_user, db, profile_id, education)

@router.put("/{profile_id}/educations/{education_id}", response_model=models.EducationResponse)
@require_any_role([Role.CANDIDATE])
def update_education(db: DbSession, profile_id: UUID, education_id: UUID, education: models.EducationRequest, current_user: CurrentUser):
    return service.update_education(current_user, db, profile_id, education_id, education)


@router.delete("/{profile_id}/educations/{education_id}", status_code=204)
@require_any_role([Role.CANDIDATE])
def delete_education(db: DbSession, profile_id: UUID, education_id: UUID, current_user: CurrentUser):
    return service.delete_education(current_user, db, profile_id, education_id)