from uuid import uuid4

import aiohttp
from gcloud.aio.storage import Storage

from app.file_storage.base_file_storage import FileStorage
from app.settings import Settings


class GoogleCloudFileStorage(FileStorage):
    def __init__(self, service_settings: Settings):
        super().__init__(service_settings)
        self.credentials = service_settings.GOOGLE_APPLICATION_CREDENTIALS
        self.bucket_list = service_settings.BUCKET_LIST

    async def _init_buckets(self):
        """We don`t init buckets for google cloud storage"""
        pass

    async def upload(self, file_data: bytes) -> str:
        filename = str(uuid4())
        bucket = self._get_bucket_name(str(filename))
        self._check_bucket(bucket)
        async with aiohttp.ClientSession() as session:
            client = Storage(session=session, service_file=self.credentials)
            await client.upload(bucket, filename, file_data)
        return filename

    async def download(self, filename: str) -> bytes:
        bucket = self._get_bucket_name(str(filename))
        self._check_bucket(bucket)
        async with aiohttp.ClientSession() as session:
            client = Storage(session=session, service_file=self.credentials)
            try:
                result = await client.download(bucket, filename)
            except aiohttp.ClientResponseError as e:
                raise FileNotFoundError(f"File {filename} not found: {e}")
            return result

    async def delete(self, filename: str) -> None:
        bucket = self._get_bucket_name(str(filename))
        self._check_bucket(bucket)
        async with aiohttp.ClientSession() as session:
            client = Storage(session=session, service_file=self.credentials)
            try:
                await client.delete(bucket, filename)
            except aiohttp.ClientResponseError as e:
                raise FileNotFoundError(f"File {filename} not found: {e}")
            return None

    async def _set_up(self) -> None:
        pass

    async def _teardown(self) -> None:
        pass
