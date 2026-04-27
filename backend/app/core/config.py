from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List

class Settings(BaseSettings):
    PROJECT_NAME: str = "Steganography API"
    API_V1_STR: str = "/api/v1"
    
    # Security
    SECRET_KEY: str = "default_insecure_secret_key"
    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000", "http://127.0.0.1:3000"]
    
    # Crypto settings
    AES_KEY_SIZE: int = 32 # 256 bits
    NONCE_SIZE: int = 12   # 96 bits for GCM
    
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

settings = Settings()
