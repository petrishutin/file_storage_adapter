import logging
import uuid

from fastapi import Depends, FastAPI, File, Response

from app.settings import settings
from app.file_storage import FileStorage, LocalFileStorage, S3FileStorage

logger = logging.getLogger(__name__)

app = FastAPI()


def storage():
    """Getting file storage type configured in app settings and returns file storage client instance."""
    file_storage_mapping = {
        "LocalFileStorage": LocalFileStorage,
        "S3FileStorage": S3FileStorage,
    }
    return file_storage_mapping[settings.FILE_STORAGE_SERVICE](settings)


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
