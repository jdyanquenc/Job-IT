from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, ConfigDict



class ProfileResponse(BaseModel):
    id: UUID
    description: str

class ProfileUpdate(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    description: Optional[str] = None
    # Add more fields as necessary