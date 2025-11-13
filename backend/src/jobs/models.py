from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, field_validator
from src.entities.job import EmploymentType
from fastapi import Query
from uuid import UUID


import logging

class JobFilters(BaseModel):
    country_code: str
    query: Optional[str] = None
    sector_ids: Optional[list[UUID]] = None
    salary_ranges: Optional[list[int]] = None

    sort_by: Optional[str] = "relevance"
    page: int = 1
    page_size: int = 20

    @field_validator("salary_ranges", mode="before")
    def parse_salary_ranges(cls, v):
        if not v:
            return []
        if isinstance(v, str):
            return [int(x) for x in v.split(",") if x.strip().isdigit()]
        return v


    @field_validator("sector_ids", mode="before")
    def parse_sector_ids(cls, v):
        print("sector_ids BEFORE:", type(v), v)

        if not v:
            return []
        if isinstance(v, str):
            return [UUID(x) for x in v.split(",") if x.strip()]
        return v


class JobCountsResponse(BaseModel):
    type: str
    id: str
    name: str
    count: int


class JobBase(BaseModel):
    job_title: str
    job_description: str
    responsibilities: str
    skills: str
    benefits: str
    remote: bool
    location: str
    employment_type: EmploymentType
    experience_min_years: Optional[int] = None
    salary_min: Optional[int] = None
    salary_max: Optional[int] = None
    currency_code: Optional[str] = None
    
    tags: Optional[list[str]] = None
    expires_at: Optional[datetime] = None
    contact_person: Optional[str] = None
    contact: Optional[str] = None
    


class JobCreate(JobBase):
    country_code: str  # Use country_code for creation

class JobUpdate(JobBase):
    # Replace country_code with country_id for updates
    country_code: str


class JobResponse(BaseModel):
    id: UUID 
    job_title: str 
    job_short_description: str
    remote: bool
    location: str
    employment_type: EmploymentType
    salary_min: Optional[int] = None
    salary_max: Optional[int] = None
    experience_min_years: Optional[int] = None
    currency_code: Optional[str] = None
    tags: list[str] = []

    created_at: datetime 
    expires_at: Optional[datetime] = None
    company_name: str
    company_image_url: str
    has_applied: bool

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
    country_code: str
    company_name: str
    company_image_url: str
    has_applied: bool
    
    model_config = ConfigDict(from_attributes=True)


class JobApplicantResponse(BaseModel):
    job_id: UUID
    user_id: UUID
    first_name: str
    last_name: str
    title: str
    description: str
    skills: list[str]
    location: str    
    status: str
    applied_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class JobApplicationResponse(JobResponse):
    pass


class JobRecommendationResponse(JobResponse):
    similarity_score: float
    pass



def get_job_filters(
    query: Optional[str] = Query(None),
    country_code: str = Query(...),
    sector_ids: Optional[str] = Query(None),
    salary_ranges: Optional[str] = Query(None),
) -> JobFilters:
    return JobFilters(
        query=query,
        country_code=country_code,
        sector_ids=sector_ids,
        salary_ranges=salary_ranges
    )