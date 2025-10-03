from datetime import datetime
import enum
from time import timezone
from tokenize import String
from sqlalchemy import UUID, Column, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship

from src.database.core import Base

class JobApplicationStatus(str, enum.Enum):
    Applied = "applied"
    Reviewed = "reviewed"
    Accepted = "accepted"
    Rejected = "rejected"


class JobApplication(Base):
    __tablename__ = "job_application"

    job_id = Column(UUID(as_uuid=True), ForeignKey("job_entry.id"), primary_key=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), primary_key=True)
    status = Column(Enum(JobApplicationStatus), nullable=False, default=JobApplicationStatus.Applied)
    applied_at = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc()))

    def __repr__(self):
        return f"<JobApplication(job_id='{self.job_id}', user_id='{self.user_id}')>"
