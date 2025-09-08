from uuid import UUID, uuid4
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from fastapi import HTTPException

from . import models
from src.entities.user import User
from src.exceptions import UserNotFoundError, InvalidPasswordError, PasswordMismatchError
from src.auth.service import verify_password, get_password_hash
import logging


bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')



def is_email_taken(db: Session, email: str) -> models.EmailAvailabilityResponse:
    user = db.query(User).filter(User.email == email.lower().strip()).first()
    return models.EmailAvailabilityResponse(available=user is None)


def get_user_by_id(db: Session, user_id: UUID) -> models.UserResponse:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        logging.warning(f"User not found with ID: {user_id}")
        raise UserNotFoundError(user_id)
    logging.info(f"Successfully retrieved user with ID: {user_id}")
    return user


def change_password(db: Session, user_id: UUID, password_change: models.PasswordChange) -> None:
    try:
        user = get_user_by_id(db, user_id)
        
        # Verify current password
        if not verify_password(password_change.current_password, user.password_hash):
            logging.warning(f"Invalid current password provided for user ID: {user_id}")
            raise InvalidPasswordError()
        
        # Verify new passwords match
        if password_change.new_password != password_change.new_password_confirm:
            logging.warning(f"Password mismatch during change attempt for user ID: {user_id}")
            raise PasswordMismatchError()
        
        # Update password
        user.password_hash = get_password_hash(password_change.new_password)
        db.commit()
        logging.info(f"Successfully changed password for user ID: {user_id}")
    except Exception as e:
        logging.error(f"Error during password change for user ID: {user_id}. Error: {str(e)}")
        raise


def register_user(db: Session, register_user_request: models.RegisterUserRequest) -> None:
    try:
        # Check password constraints
        if validate_password_strength(register_user_request.password) is False:
            logging.warning(f"Weak password attempt during registration for email: {register_user_request.email}")
            raise HTTPException(status_code=400, detail="Password does not meet strength requirements")
        
        #Validate if email already exists
        existing_user = db.query(User).filter(User.email == register_user_request.email.lower().strip()).first()
        if existing_user:
            logging.warning(f"Attempt to register with already taken email: {register_user_request.email}")
            raise HTTPException(status_code=400, detail="Email is already registered")
        

        create_user_model = User(
            id=uuid4(),
            email=register_user_request.email.lower().strip(),
            first_name=register_user_request.first_name,
            last_name=register_user_request.last_name,
            identification_type=register_user_request.identification_type,
            identification_number=register_user_request.identification_number.replace('.', '').strip(),
            password_hash=get_password_hash(register_user_request.password)
        )    
        db.add(create_user_model)
        db.commit()
    except Exception as e:
        logging.error(f"Failed to register user: {register_user_request.email}. Error: {str(e)}")
        raise


def validate_password_strength(password: str) -> bool:
    if len(password) < 8:
        return False
    if not any(char.isdigit() for char in password):
        return False
    if not any(char.isupper() for char in password):
        return False
    if not any(char.islower() for char in password):
        return False
    return True

def get_password_hash(password: str) -> str:
    return bcrypt_context.hash(password)