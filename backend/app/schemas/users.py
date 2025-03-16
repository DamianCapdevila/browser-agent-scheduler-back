from pydantic import BaseModel
from typing import List, Optional
from uuid import UUID
from app.schemas.tasks import TaskResponse

class UserBase(BaseModel):
    id: UUID
    full_name: Optional[str] = None

    class Config:
        from_attributes = True

class UserResponse(UserBase):
    pass  # Extend with additional fields if necessary

class UserWithTasks(UserBase):
    tasks: List[TaskResponse] = []
