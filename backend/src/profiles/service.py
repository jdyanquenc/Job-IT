import logging
from sqlalchemy import UUID
from sqlalchemy.orm import Session

from . import models
from src.auth.models import TokenData
from src.entities.user_profile import UserProfile
from src.exceptions import ProfileNotAccessibleError, ProfileNotFoundError
from src.profiles.models import ProfileResponse, ProfileUpdate


def get_profile(current_user: TokenData, db: Session, profile_id: UUID) -> ProfileResponse:

    if (current_user.role == "CANDIDATE" and current_user.get_uuid() != profile_id):
        logging.warning(f"Unauthorized access attempt by user {current_user.get_uuid()} to profile {profile_id}")
        raise ProfileNotAccessibleError(profile_id)
    

    profile = db.query(UserProfile).filter(UserProfile.id == profile_id).first()
    if not profile:
        logging.warning(f"Profile {profile_id} not found")
        raise ProfileNotFoundError(profile_id)

    return ProfileResponse(
        id=profile.id,
        description=profile.description
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