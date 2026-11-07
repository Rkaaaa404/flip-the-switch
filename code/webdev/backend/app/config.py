from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    APP_NAME: str = "NusaQC Backend"
    ENVIRONMENT: str = "development"
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:8000"
    ]
    DATABASE_URL: str = "sqlite:///./nusaqc.db"
    ENABLE_MOCK_HARDWARE: bool = True
    MODEL_DIR: str = "./models_weights"
    UPLOAD_DIR: str = "./uploads"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"

settings = Settings()