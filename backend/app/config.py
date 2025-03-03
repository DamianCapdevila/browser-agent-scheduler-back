# backend/app/config.py
from pydantic_settings import BaseSettings
import os


class Settings(BaseSettings):
    JWT_SECRET: str = os.getenv("JWT_SECRET")
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM")
    
    # Additional configuration for Supabase (or other services)
    SUPABASE_URL: str = os.getenv("SUPABASE_URL")
    SUPABASE_KEY: str = os.getenv("SUPABASE_KEY")
    
    class Config:
        env_file = ".env"  # Load environment variables from a .env file if present

# Create a singleton settings instance to import elsewhere in your project.
settings = Settings()
