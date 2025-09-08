from datetime import timedelta, datetime, timezone
from functools import wraps
from typing import Annotated, Optional
from uuid import UUID
from fastapi import Depends
from passlib.context import CryptContext
import jwt
from jwt import PyJWTError
from sqlalchemy.orm import Session
from src.entities.company_user import CompanyUser
from src.entities.user import Role, User
from . import models
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from ..exceptions import AuthenticationError, AuthorizationError
import logging
import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))


oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')
bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return bcrypt_context.hash(password)


def authenticate_user(email: str, password: str, db: Session) -> User | bool:
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.password_hash):
        logging.warning(f"Failed authentication attempt for email: {email}")
        return False
    return user


def create_access_token(email: str, user_id: UUID, role: Role, expires_delta: timedelta, company_id: Optional[UUID]) -> str:
    encode = {
        'sub': email,
        'id': str(user_id),
        'exp': datetime.now(timezone.utc) + expires_delta,
        'role': role.name,
        'company_id': str(company_id) if company_id else None
    }
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


def verify_token(token: str) -> models.TokenData:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get('id')
        role = payload.get("role")
        company_id = payload.get("company_id")
        return models.TokenData(user_id=user_id, role=role, company_id=company_id)
    except PyJWTError as e:
        logging.warning(f"Token verification failed: {str(e)}")
        raise AuthenticationError()


def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]) -> models.TokenData:
    return verify_token(token)


CurrentUser = Annotated[models.TokenData, Depends(get_current_user)]

""" def require_any_role(allowed_roles: list[Role]):
    def role_dependency(current_user: CurrentUser):
        if current_user.role not in [role.name for role in allowed_roles]:
            raise AuthorizationError()
        return current_user
    return role_dependency

AdminUser = Annotated[models.TokenData, Depends(require_any_role([Role.ADMIN]))]
CandidateUser = Annotated[models.TokenData, Depends(require_any_role([Role.CANDIDATE]))]
CompanyManagerUser = Annotated[models.TokenData, Depends(require_any_role([Role.COMPANY_MANAGER]))]
 """

def require_any_role(allowed_roles: list[Role]):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, current_user: CurrentUser, **kwargs):
            if current_user.role not in [role.name for role in allowed_roles]:
                raise AuthorizationError()
            return func(*args, current_user=current_user, **kwargs)
        return wrapper
    return decorator

def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                                 db: Session) -> models.Token:
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise AuthenticationError()
    
    company_user = db.query(CompanyUser).filter(CompanyUser.user_id == user.id).first() 
    company_id = company_user.company_id if company_user else None
        
    token = create_access_token(user.email, user.id, user.role, timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES), company_id)
    return models.Token(access_token=token, token_type='bearer')
