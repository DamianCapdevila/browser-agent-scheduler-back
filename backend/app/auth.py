import json
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import logging
from app.schemas.users import UserResponse
from app.config import settings  # Make sure to define settings.JWT_SECRET and settings.JWT_ALGORITHM
from app.external_services.supabase import  get_supabase_user
from jwt import decode


# Configure logger
logger = logging.getLogger("app.auth")

# Use HTTPBearer to extract the token from the Authorization header.
security = HTTPBearer()

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> UserResponse:
    token = credentials.credentials
    logger.info(f"Token: {token}")
    try:   
        user_data = await get_supabase_user(token)
        if not user_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )
        logger.info(f"User data: {user_data}")
        
        # Ensure it's a dictionary
        if hasattr(user_data, "dict"):  
            user_data = user_data.dict()  # If it's a Pydantic model
        else:
            user_data = dict(user_data)  # If it's an object
            
        # Convert the dictionary to your Pydantic model.
        user_id = user_data["id"]
        full_name = user_data["user_metadata"]["full_name"] 
        
        return UserResponse(
            id=user_id,
            full_name=full_name,
        )
    except Exception as e:
        logger.error(f"Authentication failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )
        
async def get_auth_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
    token = credentials.credentials
    return token



