from abc import ABC

from app.config import Config


class FileStorage(ABC):
    def __init__(self, service_settings: Config):
        pass

    async def upload(self, bucket_name: str, filename: str, file_data: bytes) -> bool:
        raise NotImplementedError

    async def download(self, bucket_name: str, filename: str) -> bytes:
        raise NotImplementedError
