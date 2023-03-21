import contextvars
import os
import shutil
import uuid

import pytest

import app.file_storage
from tests.conftest import get_settings_override

file_storage_service_type: contextvars.ContextVar = contextvars.ContextVar("LocalFileStorage")


@pytest.fixture(
    scope="function",
    params=["LocalFileStorage", "S3FileStorage"],
)
def storage(request):
    file_storage_service_type.set(request.param)
    store = getattr(app.file_storage, request.param)(
        get_settings_override()
    )
    yield store
    try:
        shutil.rmtree(os.getcwd() + "/storage_test")
    except FileNotFoundError:
        pass


@pytest.mark.asyncio
async def test_store_and_get(storage):
    """Smoke test. Just store and get back"""
    with open("assets/cat.jpg", "rb") as f:
        file_data = f.read()
    filename = str(uuid.uuid4())
    assert await storage.upload("main", filename, file_data)
    stored_file = await storage.download("main", filename)
    assert stored_file == file_data


@pytest.mark.asyncio
async def test_get_file_not_exist(storage):
    """This test shows that we need to handle FileNotFountError in web app"""
    with pytest.raises(FileNotFoundError):
        await storage.download("main", str(uuid.uuid4()))
