import logging
import os
import pathlib

from app.file_storage.base_file_storage import FileStorage
from app.settings import Settings


class LocalFileStorage(FileStorage):
    def __init__(self, service_settings: Settings):  # type: ignore # noqa
        self.storage_dir: str = os.path.join(os.getcwd(), service_settings.LOCAL_FILE_STORAGE_DIR)
        self.bucket_list: list[str] = service_settings.BUCKET_LIST
        if not os.path.exists(self.storage_dir):
            path = pathlib.Path(self.storage_dir)
            path.mkdir(parents=True)

    def _create_buket_if_not_exist(self, bucket):
        path_to_bucket = os.path.join(self.storage_dir, bucket)
        if not os.path.exists(path_to_bucket):
            path = pathlib.Path(path_to_bucket)
            path.mkdir(parents=True)

    async def _init_buckets(self):
        for bucket in self.bucket_list:
            self._create_buket_if_not_exist(bucket)

    async def upload(self, bucket_name: str, filename: str, file_data: bytes) -> bool:
        if not os.path.exists(os.path.join(self.storage_dir, bucket_name)):
            raise ValueError(f"Bucket {bucket_name} does not exist")
        try:
            with open(os.path.join(self.storage_dir, bucket_name, filename), "wb+") as file:
                file.write(file_data)
            return True
        except Exception as e:
            logging.error(f"Can not save file {filename}. Error {e}")
            return False

    async def download(self, bucket_name: str, filename: str) -> bytes:
        if not os.path.exists(os.path.join(self.storage_dir, bucket_name)):
            raise ValueError(f"Bucket {bucket_name} does not exist")
        with open(f"{self.storage_dir}/{bucket_name}/{filename}", "rb") as file:
            r = file.read()
            return r

    async def delete(self, bucket_name: str, filename: str) -> bool:
        try:
            os.remove(f"{self.storage_dir}/{bucket_name}/{filename}")
            return True
        except Exception as e:
            logging.error(f"Can not delete file {filename}. Error {e}")
            return False
