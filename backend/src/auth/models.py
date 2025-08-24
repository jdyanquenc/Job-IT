from uuid import UUID
from pydantic import BaseModel, EmailStr

class RegisterUserRequest(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    password: str
    role: str | None = None  # Optional role, defaults to None if not provided

class Token(BaseModel):
    access_token: str
    token_type: str
    
class TokenData(BaseModel):
    user_id: str | None = None
    role: str | None = None
    company_id: str | None = None

    def get_uuid(self) -> UUID | None:
        if self.user_id:
            return UUID(self.user_id)
        return None
    
    def get_company_uuid(self) -> UUID | None:
        if self.company_id:
            return UUID(self.company_id)
        return None