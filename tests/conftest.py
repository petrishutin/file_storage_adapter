import asyncio
import contextvars
import os

import dotenv
import pytest
from fastapi.testclient import TestClient

import app.file_storage as file_storage
from app.file_storage import FileStorage
from app.main import app as test_app
from app.main import get_settings
from app.settings import Settings

if targets_from_env := os.environ.get("TEST_TARGETS", None):
    TEST_TARGETS = [i.strip() for i in targets_from_env.split(",")]
else:
    TEST_TARGETS = ["LocalFileStorage", "S3FileStorage", "GoogleCloudFileStorage"]

file_storage_service_type: contextvars.ContextVar = contextvars.ContextVar("LocalFileStorage")


def get_settings_override():
    return Settings(
        FILE_STORAGE_TYPE=file_storage_service_type.get(),
        LOCAL_FILE_STORAGE_DIR=os.path.join(os.getcwd(), "storage_test"),
        BUCKETS=os.getenv("BUCKETS"),
    )


@pytest.fixture(scope="module", params=TEST_TARGETS)
def client(request):
    dotenv.load_dotenv(dotenv_path=".env")
    file_storage_service_type.set(request.param)
    test_app.dependency_overrides[get_settings] = get_settings_override  # type: ignore # noqa
    store: FileStorage = getattr(file_storage, request.param)(get_settings_override())
    asyncio.run(store._set_up())  # noqa
    with TestClient(test_app) as client:
        yield client
    asyncio.run(store._teardown())  # noqa
