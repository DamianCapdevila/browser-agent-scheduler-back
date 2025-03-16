from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from uuid import UUID

class TaskBase(BaseModel):
    task: str = "Unknown task"
    scheduled_time: datetime
    timezone: str = "UTC"
    status: str = "scheduled"
    result: Optional[str] = None
    error: Optional[str] = None

    class Config:
        from_attributes = True
        populate_by_name = True


class TaskCreate(TaskBase):
    user_id: UUID = Field(alias="userId")

class TaskUpdate(TaskBase):
    id: UUID
    task: str = "Unknown task"
    scheduled_time: datetime
    timezone: str = "UTC"
    status: str = "scheduled"
    result: Optional[str] = None
    error: Optional[str] = None
    
class TaskRun(TaskBase):
    id: UUID
    task: str = "Unknown task"
    scheduled_time: datetime
    timezone: str = "UTC"
    status: str = "scheduled"
    result: Optional[str] = None
    error: Optional[str] = None
    
class TaskResponse(TaskBase):
    id: str
    user_id: str
    task: str
    scheduled_time: datetime
    timezone: str
    status: str
    result: str | None
    error: str | None

