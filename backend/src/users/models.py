from pydantic import BaseModel, EmailStr
from uuid import UUID
from datetime import datetime


class EmailAvailabilityResponse(BaseModel):
    available: bool


class RegisterUserRequest(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    password: str
    identification_type: str
    identification_number: str
    role: str | None = None  # Optional role, defaults to None if not provided



class UserResponse(BaseModel):
    id: UUID
    email: EmailStr
    first_name: str
    last_name: str


class PasswordChange(BaseModel):
    current_password: str
    new_password: str
    new_password_confirm: str
