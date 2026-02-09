from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # App Settings
    APP_NAME: str = "Heimdall"
    DEBUG: bool = False
    
    # Database Settings
    DATABASE_URL: str  #cargará from variable de entorno
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # Telemetry Settings
    GRPC_PORT: int = 50051
    
    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()