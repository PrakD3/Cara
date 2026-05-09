from pydantic_settings import BaseSettings
from pydantic import ConfigDict
import os

class Settings(BaseSettings):
    model_config = ConfigDict(case_sensitive=True)

    PROJECT_NAME: str = "CARA API"
    VERSION: str = "1.0.0"

    DATABASE_URL: str = "postgresql://cara:cara_password@localhost/cara_db"
    TEST_DATABASE_URL: str = "sqlite:///./test.db"

    SECRET_KEY: str = "super_secret_fallback_key_for_dev_only"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440

    REDIS_URL: str = "redis://localhost:6379/0"

    GROQ_API_KEY: str = ""
    WISPR_API_KEY: str = ""
    GEMINI_API_KEY: str = ""

    IVR_SID: str = ""
    IVR_AUTH_TOKEN: str = ""
    IVR_WEBHOOK_URL: str = "http://localhost:8000/api/ivr/exotel/callback"

    WHATSAPP_API_KEY: str = ""
    FCM_SERVER_KEY: str = ""

settings = Settings()
