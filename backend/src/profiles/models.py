from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, ConfigDict



class ProfileResponse(BaseModel):
    id: UUID
    full_name: str
    title: str
    description: str
    location: str
    salary_range: str
    modality: str
    skills: list[str] = []
    education_experiences: list['EducationResponse'] = []
    work_experiences: list['WorkExperienceResponse'] = []

class ProfileUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    location: Optional[str] = None
    salary_range: Optional[str] = None
    modality: Optional[str] = None
    skills: Optional[list[str]] = []

class WorkExperienceRequest(BaseModel):
    company_id: Optional[UUID] = None
    company_name: str
    position: str
    start_date: datetime
    end_date: Optional[datetime] = None
    description: Optional[str] = None

class WorkExperienceResponse(WorkExperienceRequest):
    id: UUID


class EducationRequest(BaseModel):
    institution_id: Optional[UUID] = None
    institution_name: str
    degree: str
    field_of_study: str
    start_date: datetime
    end_date: Optional[datetime] = None
    description: Optional[str] = None

class EducationResponse(EducationRequest):
    id: UUID