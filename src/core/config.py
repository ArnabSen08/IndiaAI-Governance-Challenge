"""
Configuration management for the Multi-Agent AI System.
Handles environment variables, validation, and default settings.
"""

import os
from typing import Optional, Dict, Any
from pathlib import Path
from dotenv import load_dotenv
from pydantic import BaseModel, Field, field_validator, ConfigDict

# Load environment variables
load_dotenv()

class Config(BaseModel):
    """System configuration with validation and defaults."""
    
    model_config = ConfigDict(
        env_file=".env",
        case_sensitive=False
    )
    
    # API Configuration
    openai_api_key: str = Field(..., min_length=1)
    openai_model: str = Field(default="gpt-4")
    
    # System Configuration
    max_retries: int = Field(default=3, ge=1, le=10)
    timeout_seconds: int = Field(default=30, ge=5, le=300)
    max_iterations: int = Field(default=10, ge=1, le=50)
    rate_limit_requests: int = Field(default=60, ge=1)
    rate_limit_window: int = Field(default=60, ge=1)
    
    # Logging Configuration
    log_level: str = Field(default="INFO")
    log_file: str = Field(default="logs/app.log")
    enable_file_logging: bool = Field(default=True)
    
    # Security Configuration
    enable_input_validation: bool = Field(default=True)
    enable_output_filtering: bool = Field(default=True)
    max_input_length: int = Field(default=10000, ge=100)
    allowed_file_types: str = Field(default="txt,md,json")
    
    # Monitoring Configuration
    enable_metrics: bool = Field(default=True)
    health_check_interval: int = Field(default=30, ge=10)
    metrics_port: int = Field(default=8502, ge=1024, le=65535)
    
    # Development Configuration
    debug_mode: bool = Field(default=False)
    enable_profiling: bool = Field(default=False)
    
    def __init__(self, **kwargs):
        # Override with environment variables
        env_values = {
            "openai_api_key": os.getenv("OPENAI_API_KEY", ""),
            "openai_model": os.getenv("OPENAI_MODEL", "gpt-4"),
            "max_retries": int(os.getenv("MAX_RETRIES", "3")),
            "timeout_seconds": int(os.getenv("TIMEOUT_SECONDS", "30")),
            "max_iterations": int(os.getenv("MAX_ITERATIONS", "10")),
            "rate_limit_requests": int(os.getenv("RATE_LIMIT_REQUESTS", "60")),
            "rate_limit_window": int(os.getenv("RATE_LIMIT_WINDOW", "60")),
            "log_level": os.getenv("LOG_LEVEL", "INFO"),
            "log_file": os.getenv("LOG_FILE", "logs/app.log"),
            "enable_file_logging": os.getenv("ENABLE_FILE_LOGGING", "true").lower() == "true",
            "enable_input_validation": os.getenv("ENABLE_INPUT_VALIDATION", "true").lower() == "true",
            "enable_output_filtering": os.getenv("ENABLE_OUTPUT_FILTERING", "true").lower() == "true",
            "max_input_length": int(os.getenv("MAX_INPUT_LENGTH", "10000")),
            "allowed_file_types": os.getenv("ALLOWED_FILE_TYPES", "txt,md,json"),
            "enable_metrics": os.getenv("ENABLE_METRICS", "true").lower() == "true",
            "health_check_interval": int(os.getenv("HEALTH_CHECK_INTERVAL", "30")),
            "metrics_port": int(os.getenv("METRICS_PORT", "8502")),
            "debug_mode": os.getenv("DEBUG_MODE", "false").lower() == "true",
            "enable_profiling": os.getenv("ENABLE_PROFILING", "false").lower() == "true",
        }
        
        # Merge with provided kwargs
        env_values.update(kwargs)
        super().__init__(**env_values)
    
    @field_validator("log_level")
    @classmethod
    def validate_log_level(cls, v):
        valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        if v.upper() not in valid_levels:
            raise ValueError(f"Log level must be one of: {valid_levels}")
        return v.upper()
    
    @field_validator("openai_api_key")
    @classmethod
    def validate_api_key(cls, v):
        if not v or v == "your_openai_api_key_here":
            raise ValueError("OpenAI API key must be provided")
        return v
    
    def get_allowed_file_types(self) -> list:
        """Get list of allowed file types."""
        return [ext.strip() for ext in self.allowed_file_types.split(",")]
    
    def ensure_log_directory(self):
        """Ensure log directory exists."""
        log_path = Path(self.log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert config to dictionary."""
        return self.model_dump()