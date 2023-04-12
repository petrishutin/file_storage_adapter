import os
from enum import Enum

from pydantic import BaseSettings


class FileStorageService(str, Enum):
    """Enum for file file_storage service. Name of service should be same as class name"""

    LOCAL_FILE_STORAGE = "LocalFileStorage"
    S3_FILE_STORAGE = "S3FileStorage"


class Settings(BaseSettings):
    FILE_STORAGE_SERVICE: FileStorageService = "LocalFileStorage"  # type: ignore
    BUCKET_NAME: str = "main"  # pass bucket name at your service here

    # Local file_storage settings ----------------------------------
    LOCAL_FILE_STORAGE_DIR: str = os.getcwd() + "/app/.file_storage"

    # S3 file_storage settings -------------------------------------
    AWS_REGION_NAME: str = "us-east-1"
    AWS_ENDPOINT_URL: str = "http://localhost:4566"
    AWS_SECRET_ACCESS_KEY: str = "aaa"
    AWS_ACCESS_KEY_ID: str = "bbb"

    class Config:
        env_file = "../.env"
        env_file_encoding = "utf-8"


settings = Settings()
