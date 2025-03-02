from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from uuid import UUID

class TaskBase(BaseModel):
    user_id: UUID = Field(alias="userId")
    task: str = "Unknown task"
    scheduled_time: datetime = Field(alias="scheduledTime")
    timezone: str = "UTC"
    status: str = "scheduled"
    result: Optional[str] = None
    error: Optional[str] = None

    class Config:
        allow_population_by_field_name = True
        orm_mode = True

class TaskCreate(TaskBase):
    pass

class TaskResponse(TaskBase):
    id: str
    user_id: str
    task: str
    scheduled_time: datetime
    timezone: str
    status: str
    result: str
    error: str

