from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
import uuid
from ..database.core import Base 


class Currency(Base):
    __tablename__ = 'currency'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    code = Column(String, unique=True, nullable=True)
    name = Column(String, nullable=False)

    def __repr__(self):
        return f"<Currency(name='{self.name}', code='{self.code}')>"