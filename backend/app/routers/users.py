from fastapi import APIRouter, Depends, HTTPException
from app.dependencies import get_auth_token
from app.schemas.users import UserResponse

router = APIRouter(prefix="/users", tags=["Users"])









