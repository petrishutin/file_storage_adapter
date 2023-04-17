import asyncio
from abc import ABC
from uuid import UUID

from app.settings import Settings


class FileStorage(ABC):
    def __init__(self, service_settings: Settings):
        self.bucket_list: list[str] = service_settings.BUCKET_LIST

    def _get_bucket_name(self, filename: str) -> str:
        """Internal method for get bucket index in a list of buckets by filename"""
        return self.bucket_list[int(UUID(filename)) % len(self.bucket_list)]

    def _check_bucket(self, bucket_name):
        """Internal method for check bucket name exists"""
        if bucket_name not in self.bucket_list:
            raise BucketNotFoundError(f"Bucket {bucket_name} not found")

    async def _init_buckets(self):
        """This method for test mode only. In production init your buckets outside the application"""
        raise NotImplementedError

    async def upload(self, file_data: bytes) -> str:
        raise NotImplementedError

    async def upload_many(self, files: list[bytes]) -> list[str]:
        return await asyncio.gather(*[self.upload(*file) for file in files])

    async def download(self, filename: str) -> bytes:
        raise NotImplementedError

    async def download_many(self, filenames: list[str]) -> list[bytes]:
        return await asyncio.gather(*[self.download(filename) for filename in filenames])

    async def delete(self, filename: str) -> None:
        raise NotImplementedError

    async def delete_many(self, filenames: list[str]) -> None:
        await asyncio.gather(*[self.delete(filename) for filename in filenames])
        return None


class BucketNotFoundError(Exception):
    pass
