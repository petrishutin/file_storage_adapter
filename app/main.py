import logging
import uuid
from functools import lru_cache

from fastapi import Depends, FastAPI, File, Response

from app.config import Config
from app.file_storage.s3_file_storage import S3FileStorage

logger = logging.getLogger(__name__)

app = FastAPI()


@lru_cache()
def get_settings():
    return Config()


def s3_client():
    return S3FileStorage()


@app.post("/", status_code=201)
async def upload_data(
    file: bytes = File(), file_storage_client: S3FileStorage = Depends(s3_client)
):
    file_name = uuid.uuid4()
    await file_storage_client.upload("main", str(file_name), file)
    return file_name


@app.get("/", response_class=Response)
async def download_data(
    file_name: uuid.UUID, client: S3FileStorage = Depends(s3_client)
):
    return Response(
        await client.download("main", str(file_name)), media_type="image/jpg"
    )
