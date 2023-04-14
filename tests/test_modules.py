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
    filename = await storage.upload(file_data)
    assert uuid.UUID(filename)
    stored_file = await storage.download(filename)
    assert stored_file == file_data


@pytest.mark.asyncio
async def test_get_file_not_exist(storage):
    """This test shows that we need to handle FileNotFountError in web app"""
    with pytest.raises(FileNotFoundError):
        await storage.download(str(uuid.uuid4()))


@pytest.mark.asyncio
async def test_delete(storage):
    """Smoke test. Just store and get back"""
    with open("tests/assets/cat.jpg", "rb") as f:
        file_data = f.read()
    filename = await storage.upload(file_data)
    assert not await storage.delete(filename)
    with pytest.raises(FileNotFoundError):
        await storage.download(filename)


@pytest.mark.asyncio
async def test_delete_file_not_exist(storage):
    """This test shows that we need to handle FileNotFountError in web app"""
    with pytest.raises(FileNotFoundError):
        await storage.delete(str(uuid.uuid4()))
