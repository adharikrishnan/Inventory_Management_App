from functools import lru_cache
from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    ISSUER: str = "http://127.0.0.1:8000"
    AUDIENCE: str = "inventory-manager-users"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 2
    REFRESH_TOKEN_EXPIRE_DAYS: int = 1
    DEBUG: str = "False"
    ENVIRONMENT: str = "development"
    
    @property
    def cors_origins(self) -> list[str]:
        return ["*"] if self.DEBUG.lower() == "true" else []

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")
    
@lru_cache
def get_settings() -> Settings:
    return Settings()