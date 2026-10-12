from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
import os

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    # LLM Settings
    LLM_BASE_URL: str = Field(default="http://localhost:11434/v1", description="URL for Ollama or OpenAI-compatible endpoint")
    LLM_MODEL_NAME: str = Field(default="ollama/llama3", description="Model name identifier for CrewAI")
    OPENAI_API_KEY: str = Field(default="NA", description="API key (dummy value if local server doesn't require it)")

    # Syllabus API Settings
    SYLLABUS_API_BASE_URL: str = Field(default="https://api.youruniversity.edu/v1", description="Syllabus REST API base URL")
    SYLLABUS_API_TOKEN: str = Field(default="dummy_token", description="Bearer token for syllabus API")
    MOCK_SYLLABUS: bool = Field(default=True, description="When True, uses internal realistic academic curriculum fixture")

    # Output Settings
    OUTPUT_DIR: str = Field(default="output", description="Destination directory for generated assessment JSON files")

settings = Settings()
