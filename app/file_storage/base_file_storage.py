import asyncio
from abc import ABC

from app.settings import Settings


class FileStorage(ABC):
    def __init__(self, service_settings: Settings):
        pass

    async def _init_buckets(self):
        """This method for test mode only. In production init your buckets outside the application"""
        raise NotImplementedError

    async def upload(self, bucket_name: str, filename: str, file_data: bytes) -> bool:
        raise NotImplementedError

    async def upload_many(self, bucket_name: str, files: dict) -> list[bytes]:
        return await asyncio.gather(*[self.upload(*file) for file in files])

    async def download(self, bucket_name: str, filename: str) -> bytes:
        raise NotImplementedError

    async def download_many(self, bucket_name: str, files: dict) -> list[bytes]:
        return await asyncio.gather(*[self.download(*file) for file in files])

    async def delete(self, bucket_name: str, filename: str) -> bool:
        raise NotImplementedError

    async def delete_many(self, bucket_name: str, files: dict) -> list[bool]:
        return await asyncio.gather(*[self.delete(*file) for file in files])


class BucketNotFoundError(Exception):
    pass
