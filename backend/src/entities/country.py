from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from ..database.core import Base 


class Country(Base):
    __tablename__ = 'country'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    iso_code = Column(String, unique=True, nullable=True)
    currency_id = Column(UUID(as_uuid=True), ForeignKey("currency.id"), nullable=True)

    currency = relationship("Currency")

    def __repr__(self):
        return f"<Country(name='{self.name}', iso_code='{self.iso_code}', currency_id='{self.currency_id}')>"