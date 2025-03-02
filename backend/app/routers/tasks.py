from typing import List
from fastapi import APIRouter, Depends, HTTPException
from app.external_services.supabase import (
    fetch_tasks_by_user,
    insert_task_into_db,
    delete_task_from_db,
    update_task_in_db,
    get_task_by_id,
)
from app.schemas.tasks import TaskResponse, TaskCreate
from app.schemas.users import UserResponse
from app.auth import get_current_user, get_auth_token
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
import logging

logger = logging.getLogger("app.tasks")

security = HTTPBearer()
router = APIRouter()

@router.get("/", response_model=List[TaskResponse])
async def get_tasks(
    current_user: UserResponse = Depends(get_current_user),
    auth_token: str = Depends(get_auth_token)
):
    # Fetch only tasks that belong to the current user.
    tasks_data = await fetch_tasks_by_user(current_user.id, auth_token)
    
    # Convert each task dictionary to a TaskResponse object
    tasks = [TaskResponse(**task) for task in tasks_data]
    return tasks

@router.post("/", response_model=TaskResponse)
async def create_task(
    task: TaskCreate, 
    current_user: UserResponse = Depends(get_current_user),
    auth_token: str = Depends(get_auth_token)
):
    # Convert task to a dictionary and ensure the new task is linked to the current user
    task_data = task.dict(by_alias=False)
    task_data["user_id"] = current_user.id
    
    # Remove id field if it exists (let the database generate it)
    if "id" in task_data:
        del task_data["id"]
    
    logger.info(f"Task data: {task_data}")
    new_task = await insert_task_into_db(task_data, auth_token)
    
    if not new_task:
        raise HTTPException(status_code=500, detail="Failed to create task")
    
    # Convert the response to a TaskResponse object
    return TaskResponse(**new_task)

@router.delete("/{task_id}", response_model=dict)
async def delete_task(
    task_id: str, 
    current_user: UserResponse = Depends(get_current_user),
    auth_token: str = Depends(get_auth_token)
):
    task = await get_task_by_id(task_id, auth_token)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    # Verify the task belongs to the current user.
    if str(task["user_id"]) != str(current_user.id):
        raise HTTPException(status_code=403, detail="Not authorized to delete this task")
    await delete_task_from_db(task_id, auth_token)
    return {"message": "Task deleted successfully"}

@router.put("/{task_id}", response_model=dict)
async def update_task(
    task_id: str, 
    task: TaskCreate, 
    current_user: UserResponse = Depends(get_current_user),
    auth_token: str = Depends(get_auth_token)
):
    existing_task = await get_task_by_id(task_id, auth_token)
    if not existing_task:
        raise HTTPException(status_code=404, detail="Task not found")
    # Verify the task belongs to the current user.
    if str(existing_task["user_id"]) != str(current_user.id):
        raise HTTPException(status_code=403, detail="Not authorized to update this task")
    
    # Convert task to a dictionary
    task_dict = task.dict(by_alias=False)
    
    # Remove id field if it exists (we don't want to update the ID)
    if "id" in task_dict:
        del task_dict["id"]
    
    updated_task = await update_task_in_db(task_id, task_dict, auth_token)
    
    if not updated_task:
        raise HTTPException(status_code=500, detail="Failed to update task")
    
    return {"message": "Task updated successfully", "task": updated_task}
