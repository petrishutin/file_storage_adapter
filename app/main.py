import logging
import os
import uuid

from fastapi import Depends, FastAPI, File, Response

from app.file_storage import FileStorage, LocalFileStorage, S3FileStorage
from app.settings import settings

logger = logging.getLogger(__name__)

app = FastAPI()


def storage():
    """Getting file storage type configured in app settings and returns file storage client instance."""
    file_storage_mapping = {
        "LocalFileStorage": LocalFileStorage,
        "S3FileStorage": S3FileStorage,
    }
    print(os.environ.get("FileStorageService"))
    return file_storage_mapping[settings.FILE_STORAGE_SERVICE](settings)


@app.on_event("startup")
async def init_buckets():
    """Initializing file storage client for test mode."""
    if settings.TEST_MODE:
        client = storage()
        await client._init_buckets()  # pylint: disable=protected-access # noqa
    logger.info(f"{settings.FILE_STORAGE_SERVICE} buckets {settings.BUCKETS} inited")


@app.post("/", status_code=201)
async def upload_data(
    file: bytes = File(),
    client: FileStorage = Depends(storage),
):
    file_name = uuid.uuid4()
    try:
        await client.upload("main", str(file_name), file)
    except ValueError:
        return Response(status_code=400, content="Bucket not found")
    return file_name


@app.get("/", response_class=Response)
async def download_data(file_name: uuid.UUID, client: FileStorage = Depends(storage)):
    try:
        result = await client.download("main", str(file_name))
    except FileNotFoundError:
        return Response(status_code=404, content="File not found")
    except ValueError:
        return Response(status_code=400, content="Bucket not found")
    return Response(result, media_type="image/jpg")


@app.delete("/", status_code=204)
async def delete_data(file_name: uuid.UUID, client: FileStorage = Depends(storage)):
    try:
        await client.delete("main", str(file_name))
    except FileNotFoundError:
        return Response(status_code=404, content="File not found")
    except ValueError:
        return Response(status_code=400, content="Bucket not found")
    return Response(status_code=204)
