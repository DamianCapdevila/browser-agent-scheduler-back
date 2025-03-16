import os
import asyncio
from celery import Celery
from app.config import settings
from app.schemas.tasks import TaskRun, TaskUpdate
from app.services.agent import run_agent
from app.external_services.supabase import update_task_by_id
broker_url = settings.CELERY_BROKER_URL
result_backend = settings.CELERY_RESULT_BACKEND


celery = Celery("Browser Agent Runner", broker=broker_url, backend=result_backend)


celery.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    # 5-minute timeout (300 seconds)
    task_time_limit=300,  # hard limit
    task_soft_time_limit=270,  # soft limit, slightly shorter to allow for cleanup
)

@celery.task(name="run_task", bind=True, time_limit=300, soft_time_limit=270)
def run_task(self, task: TaskRun, api_key: str):
    """
    This task is executed when a task is scheduled to be run.
    It will run the task and update the task status.
    """
    try:
        task_description = task["task"]
        task_id = task["id"]
        
        # Create update object with all required fields
        update = TaskUpdate(
            id=task_id,
            task=task["task"],
            scheduled_time=task["scheduled_time"],
            timezone=task["timezone"],
            status="running"
        )
        
        # Create a new event loop for this task
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            # Run updates and agent in event loop with timeout
            async def run_with_timeout():
                # Set timeout for the entire operation (5 minutes)
                timeout = 300  # seconds
                
                # First update status
                await update_task_by_id(update)
                
                # Run agent with timeout
                result = await asyncio.wait_for(run_agent(api_key, task_description), timeout=timeout)
                
                # Update with completed status
                update_complete = TaskUpdate(
                    id=task_id,
                    task=task["task"],
                    scheduled_time=task["scheduled_time"],
                    timezone=task["timezone"],
                    status="completed",
                    result=result
                )
                await update_task_by_id(update_complete)
                return result
                
            result = loop.run_until_complete(run_with_timeout())
        except asyncio.TimeoutError:
            # Handle asyncio timeout
            update_timeout = TaskUpdate(
                id=task_id,
                task=task["task"],
                scheduled_time=task["scheduled_time"],
                timezone=task["timezone"],
                status="failed",
                error="Task execution timed out after 5 minutes"
            )
            loop.run_until_complete(update_task_by_id(update_timeout))
            return {"error": "Task execution timed out after 5 minutes"}
        finally:
            # Always close the loop
            loop.close()
        
        return result
    except Exception as e:
        # Handle errors
        try:
            update = TaskUpdate(
                id=task["id"],
                task=task["task"],
                scheduled_time=task["scheduled_time"],
                timezone=task["timezone"],
                status="failed",
                error=str(e)
            )
            loop = asyncio.get_event_loop()
            loop.run_until_complete(update_task_by_id(update))
        except Exception as inner_e:
            print(f"Error updating task status: {inner_e}")
            
        return {"error": str(e)}

# Function to schedule tasks using unique IDs
def schedule_unique_task(task: TaskRun, api_key: str):
    """
    Schedule a task only if it's not already in the queue.
    """
    # Use the existing unique task ID from the database
    task_id = str(task["id"])
    
    # Check if task with this ID is already in the queue
    existing_task = celery.AsyncResult(task_id)
    
    # Only schedule if not already queued or running
    if existing_task.state in ['SUCCESS', 'FAILURE', 'REVOKED'] or existing_task.state is None:
        # Schedule the task with the unique DB ID
        run_task.apply_async(args=[task, api_key], task_id=task_id)
        return {"status": "scheduled", "task_id": task_id}
    else:
        # Task is already in the queue
        return {"status": "already_scheduled", "task_id": task_id}

