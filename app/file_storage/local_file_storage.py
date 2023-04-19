import logging
import os
import pathlib
import shutil
from uuid import uuid4

from app.file_storage.base_file_storage import FileStorage
from app.settings import Settings


class LocalFileStorage(FileStorage):
    def __init__(self, service_settings: Settings):  # type: ignore # noqa
        self.storage_dir: str = os.path.join(os.getcwd(), service_settings.LOCAL_FILE_STORAGE_DIR)
        self.bucket_list: list[str] = service_settings.BUCKET_LIST
        if not os.path.exists(self.storage_dir):
            path = pathlib.Path(self.storage_dir)
            path.mkdir(parents=True)

    async def upload(self, file_data: bytes) -> str:
        filename = str(uuid4())
        bucket = self._get_bucket_name(filename)
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

    async def _set_up(self) -> None:
        if not os.path.exists(self.storage_dir):
            os.makedirs(self.storage_dir)
        for bucket in self.bucket_list:
            if not os.path.exists(os.path.join(self.storage_dir, bucket)):
                os.makedirs(os.path.join(self.storage_dir, bucket))

    async def _teardown(self) -> None:
        shutil.rmtree(self.storage_dir, ignore_errors=True)
