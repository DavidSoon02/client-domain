from pydantic import BaseModel
import uuid

class DeleteResponse(BaseModel):
    message: str
    deleted_user_id: uuid.UUID
