from sqlalchemy import Column, String, Enum
from sqlalchemy.dialects.postgresql import UUID
import uuid
import enum
from ..database.core import Base 


class Role(enum.Enum):
    ADMIN = "admin"
    CANDIDATE = "candidate"
    COMPANY_MANAGER = "company_manager"

class IdentificationType(enum.Enum):
    CC = "CC"
    CE = "CE"
    PASSPORT = "PASSPORT"
    TI = "TI"
    PEP = "PEP"


class User(Base):
    __tablename__ = 'users'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    password_hash = Column(String, nullable=False)
    identification_type = Column(Enum(IdentificationType), nullable=True)
    identification_number = Column(String, nullable=True)
    role = Column(Enum(Role), nullable=False)

    def __repr__(self):
        return f"<User(email='{self.email}', first_name='{self.first_name}', last_name='{self.last_name}')>"