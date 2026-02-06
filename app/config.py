"""
Configuration settings for the application.
"""

from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # Azure OpenAI Configuration
    azure_endpoint: str
    azure_api_key: str
    azure_deployment_id: str
    azure_api_version: str = ""
    
    # System Prompt Configuration
    use_ai102_system_prompt: bool = False
    
    # Server Configuration
    host: str = "0.0.0.0"
    port: int = 8000
    
    # Application Configuration
    debug: bool = False
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
