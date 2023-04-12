import logging
import os
import pathlib

from app.file_storage.base_file_storage import FileStorage
from app.settings import Settings


class LocalFileStorage(FileStorage):
    def __init__(self, service_settings: Settings):
        super().__init__(service_settings)
        self.storage_dir: str = service_settings.LOCAL_FILE_STORAGE_DIR
        if not os.path.exists(self.storage_dir):
            path = pathlib.Path(self.storage_dir)
            path.mkdir(parents=True)

    def _create_buket_if_not_exist(self, bucket):
        path_to_bucket = self.storage_dir + f"/{bucket}"
        if not os.path.exists(path_to_bucket):
            path = pathlib.Path(path_to_bucket)
            path.mkdir(parents=True)

    async def upload(self, bucket_name: str, filename: str, file_data: bytes) -> bool:
        self._create_buket_if_not_exist(bucket_name)
        try:
            with open(f"{self.storage_dir}/{bucket_name}/{filename}", "wb+") as file:
                file.write(file_data)
            return True
        except Exception as e:
            logging.error(f"Can not save file {filename}. Error {e}")
            return False

    async def download(self, bucket_name: str, filename: str) -> bytes:
        with open(f"{self.storage_dir}/{bucket_name}/{filename}", "rb") as file:
            r = file.read()
            return r
