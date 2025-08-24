from sqlalchemy import Column, ForeignKey, String, Float
from sqlalchemy.dialects.postgresql import UUID, JSONB
import uuid
import enum
from ..database.core import Base 


class UserProfile(Base):
    __tablename__ = 'user_profiles'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False, index=True)
    country_id = Column(UUID(as_uuid=True), ForeignKey('country.id'), nullable=False, index=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    description = Column(String, nullable=False)
    skills = Column(JSONB, nullable=True)
    education = Column(JSONB, nullable=True)
    experience = Column(JSONB, nullable=True)

    def __repr__(self):
        return f"<UserProfile(user_id='{self.user_id}')>"