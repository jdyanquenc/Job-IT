from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Enum, Text
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.orm import relationship
import enum
from datetime import datetime, timezone
from ..database.core import Base


class EmploymentType(str, enum.Enum):
    FullTime = "Full-time"
    PartTime = "Part-time"
    Contract = "Contract"


class JobEntry(Base):
    __tablename__ = "job_entry"

    id = Column(UUID(as_uuid=True), primary_key=True)
    job_title = Column(String, nullable=False)
    job_short_description = Column(String, nullable=False)
    remote = Column(Boolean)
    location = Column(String, nullable=True)
    employment_type = Column(Enum(EmploymentType), nullable=False, default=EmploymentType.FullTime)
    experience_min_years = Column(Integer, nullable=True)
    salary_min = Column(Integer, nullable=True)
    salary_max = Column(Integer, nullable=True)

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    company_id = Column(UUID(as_uuid=True), ForeignKey("company.id"), nullable=False, index=True)
    country_id = Column(UUID(as_uuid=True), ForeignKey("country.id"), nullable=False, index=True)
    currency_id = Column(UUID(as_uuid=True), ForeignKey("currency.id"), nullable=True, index=True)

    tags = Column(ARRAY(String), nullable=True)    
    expires_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, nullable=True)
    is_active = Column(Boolean, nullable=False, default=True)

    # ORM
    detail = relationship(
        "JobDetail", back_populates="entry", uselist=False, cascade="all, delete"
    )


    def __repr__(self):
        return f"<JobEntry(job_id='{self.id}', job_title='{self.job_title}', company_id='{self.company_id}', employment_type='{self.employment_type}', is_active={self.is_active})>"


class JobDetail(Base):
    __tablename__ = "job_detail"

    id = Column(
        UUID(as_uuid=True),
        ForeignKey("job_entry.id", ondelete="CASCADE"),
        primary_key=True,
    )
    job_description = Column(Text)
    responsibilities = Column(Text)
    skills = Column(Text)
    benefits = Column(Text)
    contact_person = Column(String, nullable=True)
    contact = Column(String, nullable=True)

    # ORM
    entry = relationship("JobEntry", back_populates="detail")

    def __repr__(self):
        return f"<JobDetail(job_id='{self.id}', remote={self.remote})>"
