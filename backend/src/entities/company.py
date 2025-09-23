from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
import uuid
from ..database.core import Base 


class Company(Base):
    __tablename__ = 'company'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    registration_number = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    sector = Column(String, nullable=True)
    industry = Column(String, nullable=True)
    city = Column(String, nullable=True)
    state = Column(String, nullable=True)
    zip = Column(String, nullable=True)
    image_url = Column(String, nullable=True)
    

    def __repr__(self):
        return f"<Company(name='{self.name}', registration_number='{self.registration_number}')>"