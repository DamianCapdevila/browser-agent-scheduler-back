from fastapi import APIRouter, HTTPException
from app.external_services.supabase import fetch_user_encrypted_api_key
from app.internal.admin import decrypt_api_key
from app.config import settings

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/{user_id}/api_key") 
async def get_user_api_key(user_id: str):
    encrypted_api_key = await fetch_user_encrypted_api_key(user_id)
    if not encrypted_api_key:
        raise HTTPException(status_code=404, detail="User API key not found")
    unencrypted_api_key = decrypt_api_key(encrypted_api_key[0], settings.PASSPHRASE)
    return unencrypted_api_key







