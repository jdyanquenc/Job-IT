from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
import uuid
from ..database.core import Base 


class Sector(Base):
    __tablename__ = 'sector'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, unique=True, nullable=True)
    description = Column(String, nullable=True)

    def __repr__(self):
        return f"<Sector(name='{self.name}', description='{self.description}')>"