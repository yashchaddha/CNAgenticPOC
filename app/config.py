# app/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    mongodb_uri: str
    s3_bucket: str
    aws_region: str = "ap-east-1"

    class Config:
        env_file = ".env"

settings = Settings()
