from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from uuid import UUID

class UserApiKeyBase(BaseModel):
    id: UUID
    user_id: UUID 
    encrypted_key: str 
    iv: str
    salt: str
    created_at: datetime
    
    
    class Config:
        from_attributes = True
        populate_by_name = True

class UserApiKeyRead(UserApiKeyBase):
    pass




