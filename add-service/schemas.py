from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
import uuid

class UserCreate(BaseModel):
    email: str
    password: Optional[str] = None
    first_name: str
    last_name: str
    github_id: Optional[str] = None
    role: Optional[str] = 'client'

class UserResponse(BaseModel):
    id: uuid.UUID
    email: str
    first_name: str
    last_name: str
    is_active: bool
    created_at: datetime
    updated_at: datetime
    github_id: Optional[str] = None
    role: str

    class Config:
        from_attributes = True
