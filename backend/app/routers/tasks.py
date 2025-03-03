from typing import List
from fastapi import APIRouter, Depends, HTTPException
from app.external_services.supabase import (
    fetch_tasks_by_user,
    insert_task_into_db,
    delete_task_from_db,
    update_task_in_db,
    get_task_by_id,
)
from app.schemas.tasks import TaskResponse, TaskCreate, TaskUpdate
from app.dependencies import get_auth_token
from fastapi.security import HTTPBearer
import logging

logger = logging.getLogger("app.tasks")

security = HTTPBearer()
router = APIRouter(prefix="/tasks", tags=["Tasks"])

@router.get("/", response_model=List[TaskResponse])
async def get_tasks(user_id: str, auth_token: str = Depends(get_auth_token)):
    tasks_data = await fetch_tasks_by_user(user_id, auth_token)
    tasks = [TaskResponse(**task) for task in tasks_data]
    return tasks


@router.post("/", response_model=TaskResponse)
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
