from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, ConfigDict, field_validator
from src.entities.job import EmploymentType


class SearchCompanyResponse(BaseModel):
    id: UUID
    name: str
