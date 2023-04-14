import logging

from fastapi import Depends, FastAPI, File, Request, Response
from fastapi.responses import JSONResponse

from app.file_storage import BucketNotFoundError, FileStorage, LocalFileStorage, S3FileStorage
from app.settings import settings

logger = logging.getLogger(__name__)

app = FastAPI()


def storage():
    """Getting file storage type configured in app settings and returns file storage client instance."""
    file_storage_mapping = {
        "LocalFileStorage": LocalFileStorage,
        "S3FileStorage": S3FileStorage,
    }
    return file_storage_mapping[settings.FILE_STORAGE_SERVICE](settings)


@app.exception_handler(FileNotFoundError)
async def file_not_found_handler(request: Request, exc: FileNotFoundError):
    return JSONResponse(
        status_code=404,
        content={"message": f"File not found: {exc}"},
    )


@app.exception_handler(BucketNotFoundError)
async def bucket_not_found_handler(request: Request, exc: BucketNotFoundError):
    return JSONResponse(
        status_code=404,
        content={"message": f"Bucket not found: {exc}"},
    )


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
    return await client.upload(file)


@app.get("/", response_class=Response)
async def download_data(file_name: str, client: FileStorage = Depends(storage)):
    return Response(await client.download(file_name))


@app.delete("/", status_code=204)
async def delete_data(file_name: str, client: FileStorage = Depends(storage)):
    await client.delete(file_name)
    return Response(status_code=204)
