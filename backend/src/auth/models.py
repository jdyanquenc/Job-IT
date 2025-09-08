from uuid import UUID
from pydantic import BaseModel, EmailStr


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