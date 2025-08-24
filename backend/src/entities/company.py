from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from ..database.core import Base 


class Company(Base):
    __tablename__ = 'company'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    location = Column(String, nullable=True)
    country_id = Column(UUID(as_uuid=True), ForeignKey("country.id", ondelete="RESTRICT"), nullable=False, index=True)
    image_url = Column(String, nullable=True)
    
    country = relationship("Country", uselist=False, foreign_keys=[country_id])
    

    def __repr__(self):
        return f"<Company(name='{self.name}', country_id='{self.country_id}')>"