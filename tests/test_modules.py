import asyncio
import os
import shutil
import uuid

import pytest

import app.file_storage
from app.settings import Settings


@pytest.fixture(
    scope="function",
    params=["LocalFileStorage", "S3FileStorage"],
)
def storage(request):
    test_settings = Settings(
        FILE_STORAGE_SERVICE=request.param,
        LOCAL_FILE_STORAGE_DIR="storage_test",
    )
    store = getattr(app.file_storage, request.param)(test_settings)
    asyncio.run(store._init_buckets())  # pylint: disable=protected-access # noqa
    yield store
    try:
        shutil.rmtree(os.path.join(os.getcwd(), "storage_test"))
    except FileNotFoundError:
        pass


@pytest.mark.asyncio
async def test_store_and_get(storage):
    """Smoke test. Just store and get back"""
    with open("tests/assets/cat.jpg", "rb") as f:
        file_data = f.read()
    filename = str(uuid.uuid4())
    assert await storage.upload("main", filename, file_data)
    stored_file = await storage.download("main", filename)
    assert stored_file == file_data
    await storage.delete("main", filename)


@pytest.mark.asyncio
async def test_get_file_not_exist(storage):
    """This test shows that we need to handle FileNotFountError in web app"""
    with pytest.raises(FileNotFoundError):
        await storage.download("main", str(uuid.uuid4()))


@pytest.mark.asyncio
async def test_get_bucket_not_exist(storage):
    """This test shows that we need to handle FileNotFountError in web app"""
    with pytest.raises(app.file_storage.BucketNotFoundError):
        await storage.download("not_main", str(uuid.uuid4()))


@pytest.mark.asyncio
async def test_delete(storage):
    """Smoke test. Just store and get back"""
    with open("tests/assets/cat.jpg", "rb") as f:
        file_data = f.read()
    filename = str(uuid.uuid4())
    assert await storage.upload("main", filename, file_data)
    assert await storage.delete("main", filename)
    with pytest.raises(FileNotFoundError):
        await storage.download("main", filename)
