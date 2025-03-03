
from app.schemas.tasks import TaskCreate, TaskResponse
from supabase import create_client, Client, ClientOptions
from app.config import settings
import logging

logger = logging.getLogger("app.external_services.supabase")

url: str = settings.SUPABASE_URL
key: str = settings.SUPABASE_KEY

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
    response = supabase.table("tasks").insert(task.model_dump(by_alias=False)).execute()

    if response.data and isinstance(response.data, list) and len(response.data) > 0:
        return response.data[0]    
    return None

async def delete_task_from_db(task_id: str, auth_token: str):
    supabase = get_supabase_client(auth_token)
    response = supabase.table("tasks").delete().eq("id", task_id).execute()
    
    if response.data and isinstance(response.data, list) and len(response.data) > 0:
        return response.data[0] 
    return None

async def update_task_in_db(task_id: str, task_data, auth_token: str):
    supabase = get_supabase_client(auth_token)
    response = supabase.table("tasks").update(task_data.model_dump(by_alias=False)).eq("id", task_id).execute()
    
    if response.data and isinstance(response.data, list) and len(response.data) > 0:
        return response.data[0] 
    return None



