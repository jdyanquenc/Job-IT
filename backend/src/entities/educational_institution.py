from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
import uuid
from ..database.core import Base 

class EducationalInstitution(Base):
    __tablename__ = "educational_institution"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    country_id = Column(UUID(as_uuid=True), ForeignKey("country.id"), nullable=True)

    def __repr__(self):
        return f"<EducationalInstitution(name='{self.name}', country_id='{self.country_id}')>"
