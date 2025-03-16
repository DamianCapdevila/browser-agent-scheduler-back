
from app.schemas.tasks import TaskCreate, TaskResponse, TaskUpdate
from supabase import create_client, Client
from fastapi.encoders import jsonable_encoder
from app.config import settings
from app.schemas.user_api_keys import UserApiKeyRead

# Admin functions

def get_supabase_admin_client() -> Client:
    supabase = create_client(settings.SUPABASE_URL, settings.SUPABASE_ADMIN_KEY)
    return supabase

async def fetch_all_tasks() -> list[TaskResponse]:
    supabase = get_supabase_admin_client()
    response = supabase.table("tasks").select("*").eq("status", "scheduled").order("scheduled_time", desc=True).execute()
    return response.data

async def fetch_user_encrypted_api_key(user_id: str) -> UserApiKeyRead:
    supabase = get_supabase_admin_client()
    response = supabase.table("user_api_keys").select("*").eq("user_id", user_id).execute()
    return response.data[0]

async def update_task_by_id(task: TaskUpdate) -> TaskResponse:
    supabase = get_supabase_admin_client()
    response = supabase.table("tasks").update(jsonable_encoder(task)).eq("id", task.id).execute()
    return response.data

