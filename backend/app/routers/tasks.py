from typing import List
from fastapi import APIRouter, HTTPException, status
from app.external_services.supabase import (
    fetch_all_tasks,
)
from app.schemas.tasks import TaskResponse, TaskCreate, TaskUpdate


router = APIRouter(prefix="/tasks", tags=["Tasks"])

#Admin routes

@router.get("/all", response_model=List[TaskResponse])
async def get_all_tasks():
    tasks = await fetch_all_tasks()
    return tasks

@router.post("/{task_id}/run", response_model=dict)
async def run_task(task_id: str):
    task = await run_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"message": "Task run successfully", "task": task}

