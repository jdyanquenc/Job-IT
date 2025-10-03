import enum
from sqlalchemy import Column, Enum, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
import uuid
from ..database.core import Base 


class CompanyType(str, enum.Enum):
    Client = "Client"
    ResumeReference = "ResumeReference"


class Company(Base):
    __tablename__ = 'company'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    company_type = Column(Enum(CompanyType), nullable=False, default=CompanyType.Client)
    name = Column(String, nullable=False)
    registration_number = Column(String, unique=True, nullable=True)
    description = Column(String, nullable=True)
    sector = Column(String, nullable=True)
    industry = Column(String, nullable=True)
    image_url = Column(String, nullable=True)

    city = Column(String, nullable=True)
    state = Column(String, nullable=True)
    zip = Column(String, nullable=True)
    
    country_id = Column(UUID(as_uuid=True), ForeignKey("country.id"), nullable=True, index=True)
    

    def __repr__(self):
        return f"<Company(name='{self.name}', registration_number='{self.registration_number}')>"