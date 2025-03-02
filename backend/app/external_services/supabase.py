import os
from app.schemas.tasks import TaskCreate, TaskResponse
from supabase import create_client, Client
from app.config import settings
from uuid import UUID
from datetime import datetime
import logging

logger = logging.getLogger("app.external_services.supabase")

url: str = settings.SUPABASE_URL
key: str = settings.SUPABASE_KEY

supabase: Client = create_client(url, key)

# Helper function to convert non-serializable objects to serializable types
def convert_to_serializable(obj):
    if isinstance(obj, dict):
        return {k: convert_to_serializable(v) for k, v in obj.items()}
    elif isinstance(obj, UUID):
        return str(obj)
    elif isinstance(obj, datetime):
        return obj.isoformat()
    return obj

async def fetch_user_by_id(user_id: str) -> dict:
    response = supabase.table("users").select("*").eq("id", user_id).execute()
    if response.data and isinstance(response.data, list) and len(response.data) > 0:
        return response.data[0]
    return None

async def get_supabase_user(jwt: str) -> dict:
    response = supabase.auth.get_user(jwt)
    return response.user

async def fetch_tasks_by_user(user_id: str, auth_token: str = None) -> list[TaskResponse]:
    if auth_token:
        supabase.postgrest.auth(auth_token)
    response = supabase.table("tasks").select("*").eq("user_id", user_id).execute()
    return response.data

async def fetch_tasks_from_db(auth_token: str = None):
    if auth_token:
        supabase.postgrest.auth(auth_token)
    response = supabase.table("tasks").select("*").execute()
    return response.data

async def get_task_by_id(task_id: str, auth_token: str = None) -> TaskResponse:
    if auth_token:
        supabase.postgrest.auth(auth_token)
    response = supabase.table("tasks").select("*").eq("id", task_id).execute()
    
    # Check if response.data is a list with at least one item
    if response.data and isinstance(response.data, list) and len(response.data) > 0:
        return response.data[0]  # Return the first item in the array
    
    return None

async def insert_task_into_db(task: TaskCreate, auth_token: str):
    # Convert task to a dictionary
    task_dict = task if isinstance(task, dict) else task.dict()
    # Convert non-serializable objects to serializable types
    task_dict = convert_to_serializable(task_dict)
    # set auth token
    supabase.postgrest.auth(auth_token)
    response = supabase.table("tasks").insert(task_dict).execute()
    
    # Log the response for debugging
    logger.info(f"Response: {response.data}")
    
    # Check if response.data is a list with at least one item
    if response.data and isinstance(response.data, list) and len(response.data) > 0:
        return response.data[0]  # Return the first item in the array
    
    return None

async def delete_task_from_db(task_id: str, auth_token: str):
    # set auth token
    supabase.postgrest.auth(auth_token)
    response = supabase.table("tasks").delete().eq("id", task_id).execute()
    
    # Check if response.data is a list with at least one item
    if response.data and isinstance(response.data, list) and len(response.data) > 0:
        return response.data[0]  # Return the first item in the array
    
    return None

async def update_task_in_db(task_id: str, task_data, auth_token: str):
    # Convert task to a dictionary if it's not already
    task_dict = task_data if isinstance(task_data, dict) else task_data.dict()
    # Convert non-serializable objects to serializable types
    task_dict = convert_to_serializable(task_dict)
    # set auth token
    supabase.postgrest.auth(auth_token)
    # Update the task with converted values
    response = supabase.table("tasks").update(task_dict).eq("id", task_id).execute()
    
    # Check if response.data is a list with at least one item
    if response.data and isinstance(response.data, list) and len(response.data) > 0:
        return response.data[0]  # Return the first item in the array
    
    return None



