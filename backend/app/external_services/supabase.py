
from app.schemas.tasks import TaskCreate, TaskResponse, TaskUpdate
from supabase import create_client, Client
from fastapi.encoders import jsonable_encoder
from app.config import settings
from app.schemas.user_api_keys import UserApiKeyRead



def get_supabase_client(token: str) -> Client:
    supabase = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)
    supabase.postgrest.auth(token) 
    return supabase

async def fetch_tasks_by_user(user_id: str, auth_token: str = None) -> list[TaskResponse]:
    supabase = get_supabase_client(auth_token)
    response = supabase.table("tasks").select("*").eq("user_id", user_id).execute()
    return response.data

async def get_task_by_id(task_id: str, auth_token: str = None) -> TaskResponse:
    supabase = get_supabase_client(auth_token)
    response = supabase.table("tasks").select("*").eq("id", task_id).execute()
    
    if response.data and isinstance(response.data, list) and len(response.data) > 0:
        return response.data[0] 
    return None

async def insert_task_into_db(task: TaskCreate, auth_token: str):
    supabase = get_supabase_client(auth_token)
    response = supabase.table("tasks").insert(jsonable_encoder(task, by_alias=False)).execute()

    if response.data and isinstance(response.data, list) and len(response.data) > 0:
        return response.data[0]    
    return None

async def delete_task_from_db(task_id: str, auth_token: str):
    supabase = get_supabase_client(auth_token)
    response = supabase.table("tasks").delete().eq("id", task_id).execute()
    
    if response.data and isinstance(response.data, list) and len(response.data) > 0:
        return response.data[0] 
    return None

async def update_task_in_db(task: TaskUpdate, auth_token: str):
    supabase = get_supabase_client(auth_token)
    response = supabase.table("tasks").update(jsonable_encoder(task, by_alias=False)).eq("id", task.id).execute()
    
    if response.data and isinstance(response.data, list) and len(response.data) > 0:
        return response.data[0] 
    return None


# Admin functions

def get_supabase_admin_client() -> Client:
    supabase = create_client(settings.SUPABASE_URL, settings.SUPABASE_ADMIN_KEY)
    return supabase

async def fetch_tasks_by_user_id(user_id: str) -> list[TaskResponse]:
    supabase = get_supabase_admin_client()
    response = supabase.table("tasks").select("*").eq("user_id", user_id).execute()
    return response.data

async def fetch_user_encrypted_api_key(user_id: str) -> list[UserApiKeyRead]:
    supabase = get_supabase_admin_client()
    response = supabase.table("user_api_keys").select("*").eq("user_id", user_id).execute()
    return response.data


