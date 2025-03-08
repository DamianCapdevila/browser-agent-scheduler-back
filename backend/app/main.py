from fastapi import FastAPI, Request
import logging
import time

import uvicorn
from .routers import tasks, users
from fastapi.middleware.cors import CORSMiddleware

logger = logging.getLogger("app.main")

app = FastAPI(
    title="Browser Agent Scheduler API",
    description="An API for scheduling tasks to be executed in the browser.",
    version="0.1.0"
)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    method = request.method
    path = request.url.path
    
    print(f"Request started: {method} {path}")
    logger.info(f"Request started: {method} {path}")
    
    response = await call_next(request)
    
    process_time = time.time() - start_time
    formatted_process_time = '{0:.2f}'.format(process_time)
    
    status_code = response.status_code
    print(f"Request completed: {method} {path} - Status: {status_code} - Duration: {formatted_process_time}s")
    logger.info(f"Request completed: {method} {path} - Status: {status_code} - Duration: {formatted_process_time}s")
    
    return response

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router)
app.include_router(tasks.router)


@app.get("/")
async def root():
    print("Root endpoint called")  # Direct print
    logger.debug("Root endpoint called")
    return {"message": "Hello, World!"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

