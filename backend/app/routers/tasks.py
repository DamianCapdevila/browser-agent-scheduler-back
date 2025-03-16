from typing import List
from fastapi import APIRouter, HTTPException, status
from app.external_services.supabase import (
    fetch_all_tasks,
    fetch_user_encrypted_api_key,
)
from app.internal.admin import decrypt_api_key
from app.config import settings
from app.schemas.tasks import TaskResponse, TaskCreate, TaskUpdate
from app.services.celery import run_task

router = APIRouter(prefix="/tasks", tags=["Tasks"])

#Admin routes

@router.get("/all", response_model=List[TaskResponse])
async def get_all_tasks():
    tasks = await fetch_all_tasks()
    return tasks


@router.post("/all/schedule")
async def schedule_all_tasks():
    tasks = await fetch_all_tasks()
    for task in tasks:
        encrypted_api_key = await fetch_user_encrypted_api_key(task["user_id"])
        unencrypted_api_key = decrypt_api_key(encrypted_api_key, settings.PASSPHRASE)
        run_task.apply_async(args=[task, unencrypted_api_key], eta=task["scheduled_time"])
    return {"message": "All tasks scheduled successfully"}

