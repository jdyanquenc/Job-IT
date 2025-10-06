from datetime import datetime
from time import timezone
from sqlalchemy import UUID, Column, DateTime, Float, ForeignKey

from src.database.core import Base


class JobRecommendation(Base):
    __tablename__ = "job_recommendation"

    job_id = Column(UUID(as_uuid=True), ForeignKey("job_entry.id"), primary_key=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), primary_key=True)
    similarity_score = Column(Float, nullable=False)
    recommended_at = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc()))

    def __repr__(self):
        return f"<JobRecommendation(job_id='{self.job_id}', user_id='{self.user_id}')>"
