"""Pydantic V2 settings configuration."""
from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """Application settings using Pydantic V2 BaseSettings."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    PROJECT_NAME: str = "Smart Campus IoT API"
    VERSION: str = "0.1.0"
    ENVIRONMENT: str = "dev"
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/smartcampus"
    SECRET_KEY: str = "1cce64ba724f97f1cb18a367610a52eb0449efde02fe9e2bbb56255f508e7b04"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    LOG_LEVEL: str = "INFO"
    
    # Hadoop / HDFS configurations
    HDFS_URL: str = "http://localhost:9870"
    HDFS_USER: str = "hadoop"

    # MQTT broker configurations
    MQTT_BROKER: str = "localhost"
    MQTT_PORT: int = 1883
    MQTT_TOPIC: str = "smartcampus/+/sensors/#"
    
    # DuckDNS and other allowed domains
    ALLOWED_ORIGINS: List[str] = ["*"]

settings = Settings()
