from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from app.external_services.supabase import (
    fetch_tasks_by_user,
    insert_task_into_db,
    delete_task_from_db,
    update_task_in_db,
    get_task_by_id,
    fetch_tasks_by_user_id,
    fetch_user_encrypted_api_key,
)
from app.schemas.tasks import TaskResponse, TaskCreate, TaskUpdate
from app.schemas.user_api_keys import UserApiKeyRead
from app.dependencies import get_auth_token
from fastapi.security import HTTPBearer
import logging
from app.internal.admin import decrypt_api_key
from app.config import settings
logger = logging.getLogger("app.tasks")

security = HTTPBearer()
router = APIRouter(prefix="/tasks", tags=["Tasks"])

@router.get("/", response_model=List[TaskResponse])
async def get_tasks(user_id: str, auth_token: str = Depends(get_auth_token)):
    tasks_data = await fetch_tasks_by_user(user_id, auth_token)
    tasks = [TaskResponse(**task) for task in tasks_data]
    return tasks


@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(task: TaskCreate, auth_token: str = Depends(get_auth_token)):
    new_task = await insert_task_into_db(task, auth_token)
    if not new_task:
        raise HTTPException(status_code=500, detail="Failed to create task")
    return TaskResponse(**new_task)


@router.delete("/{task_id}", response_model=dict)
async def delete_task(task_id: str, auth_token: str = Depends(get_auth_token)):
    try:
        await delete_task_from_db(task_id, auth_token)
        return {"message": "Task deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete task: {e}")
    
    
@router.put("/{task_id}", response_model=dict)
async def update_task(task: TaskUpdate, auth_token: str = Depends(get_auth_token)):
    updated_task = await update_task_in_db(task, auth_token)
    
    if not updated_task:
        raise HTTPException(status_code=500, detail="Failed to update task")
    
    return {"message": "Task updated successfully", "task": updated_task}


#Admin routes

@router.get("/{user_id}/tasks", response_model=List[TaskResponse])
async def get_tasks_by_user_id(user_id: str):
    tasks = await fetch_tasks_by_user_id(user_id)
    return tasks

@router.get("/{user_id}/api_key") 
async def get_user_api_key(user_id: str):
    encrypted_api_key = await fetch_user_encrypted_api_key(user_id)
    if not encrypted_api_key:
        raise HTTPException(status_code=404, detail="User API key not found")
    unencrypted_api_key = decrypt_api_key(encrypted_api_key[0], settings.PASSPHRASE)
    return unencrypted_api_key

@router.post("/{task_id}/run", response_model=dict)
async def run_task(task_id: str):
    task = await run_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"message": "Task run successfully", "task": task}

