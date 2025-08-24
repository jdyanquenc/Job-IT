from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, ConfigDict, field_validator
from src.entities.job import EmploymentType


class JobBase(BaseModel):
    job_title: str
    job_description: str
    experience: str
    qualifications: str
    responsibilities: str
    benefits: str
    remote: bool
    employment_type: EmploymentType
    skills_required: Optional[list[str]] = None
    salary_range: Optional[str] = None
    expires_at: Optional[datetime] = None


class JobCreate(JobBase):
    pass

class JobUpdate(JobBase):
    pass

class CompanyBasicInfo(BaseModel):
    name: str
    location: str
    country_code: str
    image_url: str


class JobResponse(BaseModel):
    id: UUID 
    job_title: str 
    job_short_description: str
    remote: bool
    employment_type: EmploymentType
    skills_required: list[str]
    salary_range: str
    created_at: datetime 
    expires_at: Optional[datetime] = None
    company: CompanyBasicInfo

    @field_validator("employment_type", mode='before')
    def normalize_employment_type(cls, v):
        if isinstance(v, str):
            mapping = {
                "FullTime": EmploymentType.FullTime,
                "PartTime": EmploymentType.PartTime,
                "Contract": EmploymentType.Contract
            }
            return mapping.get(v, v)
        return v
    
    model_config = ConfigDict(from_attributes=True)


class JobDetailResponse(JobBase):
    id: UUID
    is_active: bool
    created_at: datetime 
    company: CompanyBasicInfo
    
    model_config = ConfigDict(from_attributes=True)
