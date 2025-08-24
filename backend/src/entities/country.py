from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
import uuid
from ..database.core import Base 


class Country(Base):
    __tablename__ = 'country'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    iso_code = Column(String, unique=True, nullable=False)

    def __repr__(self):
        return f"<Country(name='{self.name}', iso_code='{self.iso_code}')>"