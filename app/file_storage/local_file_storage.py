import logging
import os
import pathlib
from uuid import uuid4

from app.file_storage.base_file_storage import BucketNotFoundError, FileStorage
from app.settings import Settings


class LocalFileStorage(FileStorage):
    def __init__(self, service_settings: Settings):  # type: ignore # noqa
        self.storage_dir: str = os.path.join(os.getcwd(), service_settings.LOCAL_FILE_STORAGE_DIR)
        self.bucket_list: list[str] = service_settings.BUCKET_LIST
        if not os.path.exists(self.storage_dir):
            path = pathlib.Path(self.storage_dir)
            path.mkdir(parents=True)

    def _create_buket_if_not_exist(self, bucket: str):
        path_to_bucket = os.path.join(self.storage_dir, bucket)
        if not os.path.exists(path_to_bucket):
            path = pathlib.Path(path_to_bucket)
            path.mkdir(parents=True)

    async def _init_buckets(self):
        for bucket in self.bucket_list:
            self._create_buket_if_not_exist(bucket)

    def _check_bucket(self, bucket_name: str):
        if not os.path.exists(os.path.join(self.storage_dir, bucket_name)):
            raise BucketNotFoundError(f"Bucket {bucket_name} does not exist")

    async def upload(self, file_data: bytes) -> str:
        filename = str(uuid4())
        bucket = self._get_bucket_name(filename)
        self._check_bucket(bucket)
        try:
            with open(os.path.join(self.storage_dir, bucket, filename), "wb+") as file:
                file.write(file_data)
            return filename
        except Exception as e:
            logging.error(f"Can not save file {filename}. Error {e}")
            raise e

    async def download(self, filename: str) -> bytes:
        bucket = self._get_bucket_name(str(filename))
        self._check_bucket(bucket)
        with open(os.path.join(self.storage_dir, bucket, filename), "rb") as file:
            r = file.read()
            return r

    async def delete(self, filename: str) -> None:
        bucket = self._get_bucket_name(filename)
        self._check_bucket(bucket)
        os.remove(os.path.join(self.storage_dir, bucket, str(filename)))
        return None
