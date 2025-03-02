from fastapi import FastAPI, Request
import logging
import logging.config
import sys
import time
from app.routers import tasks, users
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings  # your configuration module

# Configure logging
logging.config.dictConfig({
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "stream": sys.stdout,  # Explicitly set to stdout
            "level": "DEBUG",
            "formatter": "default",
        },
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": "app.log",
            "maxBytes": 10485760,  # 10MB
            "backupCount": 3,
            "formatter": "default",
            "level": "DEBUG",
        }
    },
    "loggers": {
        "app": {
            "handlers": ["console", "file"],
            "level": "DEBUG",
            "propagate": True  # Changed to True to propagate to root logger
        }
    },
    "root": {
        "handlers": ["console"],
        "level": "DEBUG",  # Set to DEBUG to see all messages
    }
})

# Get a logger for the main module
logger = logging.getLogger("app.main")

# Print a message to confirm logging is set up
print("Logging has been configured!")
logger.info("Logger initialized")

app = FastAPI(
    title="Browser Agent Scheduler",
    description="An API for scheduling tasks to be executed in the browser.",
    version="0.1.0"
)

# Add custom middleware for request logging
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

# Startup event: initialize connections, services, etc.
@app.on_event("startup")
async def startup_event():
    # For example, if you use a Supabase client, initialize it here.
    # from app.external_services.supabase import init_supabase_client
    # init_supabase_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)
    print("Starting up the application...")  # Direct print
    logger.info("Startup: initializing services...")

# Shutdown event: clean up resources if necessary.
@app.on_event("shutdown")
async def shutdown_event():
    # Clean up connections, shutdown clients, etc.
    print("Shutting down the application...")  # Direct print
    logger.info("Shutdown: cleaning up services...")

# Root endpoint
@app.get("/")
async def root():
    print("Root endpoint called")  # Direct print
    logger.debug("Root endpoint called")
    return {"message": "Hello, World!"}

# Include routers with optional prefixes and tags for documentation.
app.include_router(tasks.router, prefix="/tasks", tags=["Tasks"])
app.include_router(users.router, prefix="/users", tags=["Users"])

# Health check endpoint.
@app.get("/health")
async def health():
    print("Health check endpoint called")  # Direct print
    logger.debug("Health check endpoint called")
    return {"status": "ok"}








