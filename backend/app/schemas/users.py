from pydantic import BaseModel
from typing import List, Optional
from uuid import UUID
from app.schemas.tasks import TaskResponse  # Your task schema defined earlier

class UserBase(BaseModel):
    id: UUID
    full_name: Optional[str] = None

    class Config:
        orm_mode = True

class UserResponse(UserBase):
    pass  # Extend with additional fields if necessary

class UserWithTasks(UserBase):
    tasks: List[TaskResponse] = []
