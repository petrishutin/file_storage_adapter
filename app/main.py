import logging
import uuid
from functools import lru_cache

from fastapi import Depends, FastAPI, File, Response

from app.settings import Settings
from app.file_storage import FileStorage, LocalFileStorage, S3FileStorage

logger = logging.getLogger(__name__)

app = FastAPI()


@lru_cache()
def get_settings():
    return Settings()


def storage(config=Depends(get_settings)):
    file_storage_mapping = {
        "LocalFileStorage": LocalFileStorage,
        "S3FileStorage": S3FileStorage,
    }
    return file_storage_mapping[config.FILE_STORAGE_SERVICE](config)


@app.post("/", status_code=201)
async def upload_data(
        file: bytes = File(), client: FileStorage = Depends(storage),
):
    file_name = uuid.uuid4()
    await client.upload("main", str(file_name), file)
    return file_name


@app.get("/", response_class=Response)
async def download_data(
        file_name: uuid.UUID, client: FileStorage = Depends(storage)
):
    return Response(
        await client.download("main", str(file_name)), media_type="image/jpg"
    )
