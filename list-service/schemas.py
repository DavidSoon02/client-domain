from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional
import uuid

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

class UserListResponse(BaseModel):
    users: List[UserResponse]
    total: int
