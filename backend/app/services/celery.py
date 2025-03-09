import os
import asyncio
from celery import Celery
from app.config import settings
from app.schemas.tasks import TaskRun
from app.services.agent import run_agent

broker_url = settings.CELERY_BROKER_URL
result_backend = settings.CELERY_RESULT_BACKEND


celery = Celery("Browser Agent Runner", broker=broker_url, backend=result_backend)


celery.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
)

@celery.task(name="run_task")
def run_task(task: TaskRun, api_key: str):
    """
    This task is executed when a task is scheduled to be run.
    It will run the task and update the task status.
    """
    try:
        task_description = task["task"]
        result = asyncio.run(run_agent(api_key, task_description))
        return result
    except Exception as e:
        return {"error": str(e)}

