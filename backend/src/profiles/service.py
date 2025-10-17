import logging
from uuid import uuid4
from sqlalchemy import UUID
from sqlalchemy.orm import Session

from src.entities.company import Company, CompanyType
from src.entities.educational_institution import EducationalInstitution
from src.entities.user import User
from src.messaging.events import publish_event

from . import models
from src.auth.models import TokenData
from src.entities.user_profile import EducationExperience, UserProfile, WorkExperience
from src.exceptions import EducationExperienceBadRequestError, EducationExperienceNotAccessibleError, EducationExperienceNotAccessibleError, ProfileNotAccessibleError, ProfileNotFoundError, WorkExperienceBadRequestError, WorkExperienceFoundError, WorkExperienceNotAccessibleError
from src.profiles.models import ProfileResponse, ProfileUpdate, WorkExperienceRequest, WorkExperienceResponse


def get_profile(current_user: TokenData, db: Session, profile_id: UUID) -> ProfileResponse:

    if (current_user.role == "CANDIDATE" and current_user.get_uuid() != profile_id):
        logging.warning(f"Unauthorized access attempt by user {current_user.get_uuid()} to profile {profile_id}")
        raise ProfileNotAccessibleError(profile_id)
    

    profile = db.query(UserProfile).filter(UserProfile.id == profile_id).first()
    if not profile:
        logging.warning(f"Profile {profile_id} not found")
        raise ProfileNotFoundError(profile_id)
    
    # Fetch associated user to get additional details
    user = db.query(User).filter(User.id == profile_id).first()

    # Order education experiences by start_date descending
    if not profile.education_experiences:
        profile.education_experiences = []
    profile.education_experiences.sort(key=lambda ee: ee.start_date, reverse=True)

    # Order work experiences by start_date descending
    if not profile.work_experiences:
        profile.work_experiences = []
    profile.work_experiences.sort(key=lambda we: we.start_date, reverse=True)

    return ProfileResponse(
        id=profile.id,
        full_name=user.full_name if user and user.full_name else "",
        title=profile.title if profile.title else "",
        description=profile.description if profile.description else "",
        location=profile.location if profile.location else "",
        salary_range=profile.salary_range if profile.salary_range else "",
        modality=profile.modality if profile.modality else "",
        skills=profile.skills if profile.skills else [],
        education_experiences=[
            models.EducationResponse(
                id=ee.id,
                institution_id=ee.institution_id,
                institution_name=ee.institution_name,
                degree=ee.degree,
                field_of_study=ee.field_of_study,
                start_date=ee.start_date,
                end_date=ee.end_date,
                description=ee.description
            ) for ee in profile.education_experiences
        ],
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
    
    # Fetch associated user to get additional details
    user = db.query(User).filter(User.id == current_user.get_uuid()).first()
    
    # Update only the fields provided in the update request
    if profile_update.title is not None:
        profile.title = profile_update.title

    if profile_update.description is not None:
        profile.description = profile_update.description
    
    if profile_update.location is not None:
        profile.location = profile_update.location
    
    if profile_update.salary_range is not None:
        profile.salary_range = profile_update.salary_range
    
    if profile_update.modality is not None:
        profile.modality = profile_update.modality
    
    if profile_update.skills is not None:
        profile.skills = profile_update.skills
    
    db.commit()
    db.refresh(profile)

    publish_event("profile.updated", profile)

    logging.info(f"Profile {profile_id} updated by user {current_user.get_uuid()}")
    return ProfileResponse(
        id=profile.id,
        full_name=user.full_name if user and user.full_name else "",
        title=profile.title if profile.title else "",
        description=profile.description if profile.description else "",
        location=profile.location if profile.location else "",
        salary_range=profile.salary_range if profile.salary_range else "",
        modality=profile.modality if profile.modality else "",
        skills=profile.skills if profile.skills else []
    )


def add_working_experience(current_user: TokenData, db: Session, profile_id: UUID, work_experience: WorkExperienceRequest) -> WorkExperienceResponse:
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


def update_working_experience(current_user: TokenData, db: Session, profile_id: UUID, experience_id: UUID, work_experience: WorkExperienceRequest) -> WorkExperienceResponse:
    if current_user.get_uuid() != profile_id:
        logging.warning(f"Unauthorized work experience update attempt by user {current_user.get_uuid()} to experience {experience_id}")
        raise WorkExperienceNotAccessibleError(experience_id)

    experience = db.query(WorkExperience).filter(WorkExperience.id == experience_id).filter(WorkExperience.user_profile_id == profile_id).first()
    if not experience:
        logging.warning(f"Work experience {experience_id} not found for update")
        raise WorkExperienceFoundError(experience_id)
   
    # Update only the fields provided in the update request
    if work_experience.company_id:
        existing_company = db.query(Company).filter(Company.id == work_experience.company_id).first()
        if not existing_company:
            logging.warning(f"Company {work_experience.company_id} not found for work experience update")
            raise WorkExperienceBadRequestError(f"Company {work_experience.company_id} not found")
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


def add_education(current_user: TokenData, db: Session, profile_id: UUID, education: models.EducationRequest) -> models.EducationResponse:
    if current_user.get_uuid() != profile_id:
        logging.warning(f"Unauthorized education addition attempt by user {current_user.get_uuid()} to profile {profile_id}")
        raise EducationExperienceNotAccessibleError(profile_id)
    
    profile = db.query(UserProfile).filter(UserProfile.id == profile_id).first()
    if not profile:
        logging.warning(f"Profile {profile_id} not found for adding education")
        raise ProfileNotFoundError(profile_id)

    # Check if institution_id is provided else create a new institution entry
    if not education.institution_id:
        new_institution = EducationalInstitution(
            id=uuid4(),
            name=education.institution_name
        )
        db.add(new_institution)
        db.commit()
        db.refresh(new_institution)
        education.institution_id = new_institution.id
    else:
        existing_institution = db.query(EducationalInstitution).filter(EducationalInstitution.id == education.institution_id).first()
        if not existing_institution:
            logging.warning(f"Institution {education.institution_id} not found for education addition")
            raise EducationExperienceBadRequestError(f"Institution {education.institution_id} not found")
        
        education.institution_id = existing_institution.id
        education.institution_name = existing_institution.name

    new_education = EducationExperience(
        id=uuid4(),
        institution_id=education.institution_id,
        institution_name=education.institution_name,
        degree=education.degree,
        field_of_study=education.field_of_study,
        start_date=education.start_date,
        end_date=education.end_date,
        description=education.description
    )
    profile.education_experiences.append(new_education)
    
    db.commit()
    db.refresh(profile)

    logging.info(f"Education added to profile {profile_id} by user {current_user.get_uuid()}")
    return models.EducationResponse(
        id=new_education.id,
        institution_id=new_education.institution_id,
        institution_name=new_education.institution_name,
        degree=new_education.degree,
        field_of_study=new_education.field_of_study,
        start_date=new_education.start_date,
        end_date=new_education.end_date,
        description=new_education.description
    )


def update_education(current_user: TokenData, db: Session, profile_id: UUID, education_id: UUID, education: models.EducationRequest) -> models.EducationResponse:
    if current_user.get_uuid() != profile_id:
        logging.warning(f"Unauthorized education update attempt by user {current_user.get_uuid()} to education {education_id}")
        raise EducationExperienceNotAccessibleError(education_id)

    education_exp = db.query(EducationExperience).filter(EducationExperience.id == education_id).filter(EducationExperience.user_profile_id == profile_id).first()
    if not education_exp:
        logging.warning(f"Education experience {education_id} not found for update")
        raise EducationExperienceNotAccessibleError(education_id)
   
    # Update only the fields provided in the update request
    if education.institution_id:
        existing_institution = db.query(EducationalInstitution).filter(EducationalInstitution.id == education.institution_id).first()
        if not existing_institution:
            logging.warning(f"Institution {education.institution_id} not found for education update")
            raise EducationExperienceBadRequestError(f"Institution {education.institution_id} not found")
        education_exp.institution_id = existing_institution.id
        education_exp.institution_name = existing_institution.name
    
    if education.institution_name:
        education_exp.institution_name = education.institution_name
    if education.degree:
        education_exp.degree = education.degree
    if education.field_of_study:
        education_exp.field_of_study = education.field_of_study
    if education.start_date:
        education_exp.start_date = education.start_date
    if education.end_date:
        education_exp.end_date = education.end_date
    if education.description:
        education_exp.description = education.description

    db.commit()
    db.refresh(education_exp)

    logging.info(f"Education experience {education_id} updated by user {current_user.get_uuid()}")
    return models.EducationResponse(
        id=education_exp.id,
        institution_id=education_exp.institution_id,
        institution_name=education_exp.institution_name,
        degree=education_exp.degree,
        field_of_study=education_exp.field_of_study,
        start_date=education_exp.start_date,
        end_date=education_exp.end_date,
        description=education_exp.description
    )


def delete_education(current_user: TokenData, db: Session, profile_id: UUID, education_id: UUID) -> None:
    if current_user.get_uuid() != profile_id:
        logging.warning(f"Unauthorized education deletion attempt by user {current_user.get_uuid()} to education {education_id}")
        raise EducationExperienceNotAccessibleError(education_id)

    education_exp = db.query(EducationExperience).filter(EducationExperience.id == education_id).filter(EducationExperience.user_profile_id == profile_id).first()
    if not education_exp:
        logging.warning(f"Education experience {education_id} not found for deletion")
        raise EducationExperienceNotAccessibleError(education_id)
    
    db.delete(education_exp)
    db.commit()

    logging.info(f"Education experience {education_id} deleted by user {current_user.get_uuid()}")
    return