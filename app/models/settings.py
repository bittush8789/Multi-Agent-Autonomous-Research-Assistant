from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    GROQ_API_KEY: Optional[str] = None
    TAVILY_API_KEY: Optional[str] = None
    REDIS_URL: str = "redis://localhost:6379/0"
    MODEL_NAME: str = "llama-3.3-70b-versatile"
    CHROMA_DB_PATH: str = "./vector_store"
    UPLOAD_DIR: str = "./uploads"
    REPORT_DIR: str = "./reports"
    DEBUG: bool = True

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

settings = Settings()
