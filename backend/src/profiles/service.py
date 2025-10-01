import logging
from uuid import uuid4
from sqlalchemy import UUID
from sqlalchemy.orm import Session

from src.entities.company import Company, CompanyType

from . import models
from src.auth.models import TokenData
from src.entities.user_profile import UserProfile, WorkExperience
from src.exceptions import ProfileNotAccessibleError, ProfileNotFoundError
from src.profiles.models import ProfileResponse, ProfileUpdate, WorkExperienceRequest, WorkExperienceResponse


def get_profile(current_user: TokenData, db: Session, profile_id: UUID) -> ProfileResponse:

    if (current_user.role == "CANDIDATE" and current_user.get_uuid() != profile_id):
        logging.warning(f"Unauthorized access attempt by user {current_user.get_uuid()} to profile {profile_id}")
        raise ProfileNotAccessibleError(profile_id)
    

    profile = db.query(UserProfile).filter(UserProfile.id == profile_id).first()
    if not profile:
        logging.warning(f"Profile {profile_id} not found")
        raise ProfileNotFoundError(profile_id)

    # Order work experiences by start_date descending
    profile.work_experiences.sort(key=lambda we: we.start_date, reverse=True)

    return ProfileResponse(
        id=profile.id,
        description=profile.description,
        work_experiences=[
            WorkExperienceResponse(
                id=we.id,
                company_id=we.company_id,
                company_name=we.company_name,
                position=we.position,
                start_date=we.start_date,
                end_date=we.end_date,
                description=we.description
            ) for we in profile.work_experiences
        ]
    )


def update_profile(current_user: TokenData, db: Session, profile_id: UUID, profile_update: ProfileUpdate) -> ProfileResponse:
    if current_user.get_uuid() != profile_id:
        logging.warning(f"Unauthorized update attempt by user {current_user.get_uuid()} to profile {profile_id}")
        raise ProfileNotAccessibleError(profile_id)
    
    profile = db.query(UserProfile).filter(UserProfile.id == profile_id).first()
    if not profile:
        logging.warning(f"Profile {profile_id} not found for update")
        raise ProfileNotFoundError(profile_id)
    
    # Update only the fields provided in the update request
    if profile_update.description:
        profile.description = profile_update.description
        # Add more fields as necessary
    
    db.commit()
    db.refresh(profile)

    logging.info(f"Profile {profile_id} updated by user {current_user.get_uuid()}")
    return ProfileResponse(
        id=profile.id,
        description=profile.description
    )

def add_working_experience(current_user: TokenData, db: Session, profile_id: UUID, work_experience: models.WorkExperienceRequest) -> WorkExperienceResponse:
    if current_user.get_uuid() != profile_id:
        logging.warning(f"Unauthorized work experience addition attempt by user {current_user.get_uuid()} to profile {profile_id}")
        raise ProfileNotAccessibleError(profile_id)
    
    profile = db.query(UserProfile).filter(UserProfile.id == profile_id).first()
    if not profile:
        logging.warning(f"Profile {profile_id} not found for adding work experience")
        raise ProfileNotFoundError(profile_id)

    # Check if company_id is provided else create a new company entry
    if not work_experience.company_id:
        new_company = Company(
            id=uuid4(),
            name=work_experience.company_name,
            company_type=CompanyType.ResumeReference
        )
        db.add(new_company)
        db.commit()
        db.refresh(new_company)
        work_experience.company_id = new_company.id
    else:
        existing_company = db.query(Company).filter(Company.id == work_experience.company_id).first()
        if not existing_company:
            logging.warning(f"Company {work_experience.company_id} not found for work experience addition")
            raise ProfileNotAccessibleError(f"Company {work_experience.company_id} not found")
        
        work_experience.company_id = existing_company.id
        work_experience.company_name = existing_company.name

    new_experience = WorkExperience(
        id=uuid4(),
        company_id=work_experience.company_id,
        company_name=work_experience.company_name,
        position=work_experience.position,
        start_date=work_experience.start_date,
        end_date=work_experience.end_date,
        description=work_experience.description
    )
    profile.work_experiences.append(new_experience)
    
    db.commit()
    db.refresh(profile)

    logging.info(f"Work experience added to profile {profile_id} by user {current_user.get_uuid()}")
    return WorkExperienceResponse(
        id=new_experience.id,
        company_id=new_experience.company_id,
        company_name=new_experience.company_name,
        position=new_experience.position,
        start_date=new_experience.start_date,
        end_date=new_experience.end_date,
        description=new_experience.description
    )


def update_working_experience(current_user: TokenData, db: Session, profile_id: UUID, experience_id: UUID, work_experience: models.WorkExperienceRequest) -> WorkExperienceResponse:
    if current_user.get_uuid() != profile_id:
        logging.warning(f"Unauthorized work experience update attempt by user {current_user.get_uuid()} to experience {experience_id}")
        raise ProfileNotAccessibleError(experience_id)

    experience = db.query(WorkExperience).filter(WorkExperience.id == experience_id).filter(WorkExperience.user_profile_id == profile_id).first()
    if not experience:
        logging.warning(f"Work experience {experience_id} not found for update")
        raise ProfileNotFoundError(experience_id)
   
    # Update only the fields provided in the update request
    if work_experience.company_id:
        existing_company = db.query(Company).filter(Company.id == work_experience.company_id).first()
        if not existing_company:
            logging.warning(f"Company {work_experience.company_id} not found for work experience update")
            raise ProfileNotAccessibleError(f"Company {work_experience.company_id} not found")
        experience.company_id = existing_company.id
        experience.company_name = existing_company.name
    
    if work_experience.company_name:
        experience.company_name = work_experience.company_name
    if work_experience.position:
        experience.position = work_experience.position
    if work_experience.start_date:
        experience.start_date = work_experience.start_date
    if work_experience.end_date:
        experience.end_date = work_experience.end_date
    if work_experience.description:
        experience.description = work_experience.description

    db.commit()
    db.refresh(experience)

    logging.info(f"Work experience {experience_id} updated by user {current_user.get_uuid()}")
    return WorkExperienceResponse(
        id=experience.id,
        company_id=experience.company_id,
        company_name=experience.company_name,
        position=experience.position,
        start_date=experience.start_date,
        end_date=experience.end_date,
        description=experience.description
    )


def delete_working_experience(current_user: TokenData, db: Session, profile_id: UUID, experience_id: UUID) -> None:
    if current_user.get_uuid() != profile_id:
        logging.warning(f"Unauthorized work experience deletion attempt by user {current_user.get_uuid()} to experience {experience_id}")
        raise ProfileNotAccessibleError(experience_id)

    experience = db.query(WorkExperience).filter(WorkExperience.id == experience_id).filter(WorkExperience.user_profile_id == profile_id).first()
    if not experience:
        logging.warning(f"Work experience {experience_id} not found for deletion")
        raise ProfileNotFoundError(experience_id)
    
    db.delete(experience)
    db.commit()

    logging.info(f"Work experience {experience_id} deleted by user {current_user.get_uuid()}")
    return