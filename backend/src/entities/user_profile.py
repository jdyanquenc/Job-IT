from sqlalchemy import Column, Date, Enum, ForeignKey, String, Float, Text
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID, JSONB
import uuid
import enum
from ..database.core import Base 


class DegreeType(str, enum.Enum):
    HighSchool = "High School"
    Associate = "Associate"
    Bachelor = "Bachelor"
    Specialization = "Specialization"
    Master = "Master"
    Doctorate = "Doctorate"
    Other = "Other"


class WorkExperience(Base):
    __tablename__ = "work_experience"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_profile_id = Column(UUID(as_uuid=True), ForeignKey("user_profile.id"), nullable=False)
    company_id = Column(UUID(as_uuid=True), ForeignKey("company.id"), nullable=True)
    company_name = Column(String, nullable=True)
    position = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=True) # Null if currently working

    # ORM
    user_profile = relationship("UserProfile", back_populates="work_experiences")

    def __repr__(self):
        return (
            f"<WorkExperience(id={self.id}, position={self.position}, "
            f"company_name={self.company_name}, start_date={self.start_date}, end_date={self.end_date})>"
        )
    

class EducationExperience(Base):
    __tablename__ = "education_experience"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_profile_id = Column(UUID(as_uuid=True), ForeignKey("user_profile.id"), nullable=False)
    institution_name = Column(String, nullable=True)
    institution_id = Column(UUID(as_uuid=True), ForeignKey("educational_institution.id"), nullable=True)
    degree = Column(Enum(DegreeType), nullable=False)
    field_of_study = Column(String, nullable=True)
    description = Column(Text, nullable=True)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=True) # Null if currently studying

    # ORM
    user_profile = relationship("UserProfile", back_populates="education_experiences")

    def __repr__(self):
        return (
            f"<EducationExperience(id={self.id}, institution={self.institution_name}, "
            f"degree={self.degree}, program={self.program}, "
            f"start_date={self.start_date}, end_date={self.end_date})>"
        )

class UserProfile(Base):
    __tablename__ = 'user_profile'

    id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True,
    )
    country_id = Column(UUID(as_uuid=True), ForeignKey('country.id'), nullable=True, index=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    description = Column(String, nullable=True)
    skills = Column(JSONB, nullable=True)

    work_experiences = relationship("WorkExperience", back_populates="user_profile")
    education_experiences = relationship("EducationExperience", back_populates="user_profile")

    def __repr__(self):
        return f"<UserProfile(user_id='{self.user_id}')>"
    
