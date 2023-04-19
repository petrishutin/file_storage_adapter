import os
from enum import Enum

from pydantic import BaseSettings


class FileStorageService(str, Enum):
    """Enum for file file_storage service. Name of service should be same as class name"""

    LOCAL_FILE_STORAGE = "LocalFileStorage"
    S3_FILE_STORAGE = "S3FileStorage"
    GOOGLE_CLOUD_STORAGE = "GoogleCloudFileStorage"


class Settings(BaseSettings):
    TEST_MODE: int = 0
    FILE_STORAGE_TYPE: FileStorageService = "LocalFileStorage"  # type: ignore
    # pass bucket names separated by comma at your cloud service here
    BUCKETS: str = os.getenv("BUCKETS")  # type: ignore
    BUCKET_LIST: list[str] = [i.strip() for i in BUCKETS.split(",")]  # type: ignore

    # Local file_storage settings ----------------------------------
    LOCAL_FILE_STORAGE_DIR: str = os.path.join(os.getcwd(), ".local_file_storage")

    # S3 file_storage settings -------------------------------------
    AWS_REGION_NAME: str = "us-east-1"
    AWS_ENDPOINT_URL: str = "http://localhost:4566"
    AWS_SECRET_ACCESS_KEY: str = "access_key"
    AWS_ACCESS_KEY_ID: str = "secret_key"

    # Google Cloud Storage settings -------------------------------------
    GOOGLE_APPLICATION_CREDENTIALS: str = "project-credentials.json"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
