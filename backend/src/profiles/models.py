from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, ConfigDict



class ProfileResponse(BaseModel):
    id: UUID
    description: str
    work_experiences: list['WorkExperienceResponse'] = []

class ProfileUpdate(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    description: Optional[str] = None
    # Add more fields as necessary

class WorkExperienceRequest(BaseModel):
    company_id: Optional[UUID] = None
    company_name: str
    position: str
    start_date: datetime
    end_date: Optional[datetime] = None
    description: Optional[str] = None

class WorkExperienceResponse(WorkExperienceRequest):
    id: UUID