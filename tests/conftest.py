import contextvars
import os
import shutil

import pytest
from fastapi.testclient import TestClient

from app.main import app, get_settings
from app.settings import Settings


if targets_from_env := os.environ.get("TEST_TARGETS", None):
    TEST_TARGETS = [i.strip() for i in targets_from_env.split(",")]
else:
    TEST_TARGETS = ["LocalFileStorage", "S3FileStorage", "GoogleCloudFileStorage"]

file_storage_service_type: contextvars.ContextVar = contextvars.ContextVar("LocalFileStorage")


def get_settings_override():
    return Settings(
        FILE_STORAGE_SERVICE=file_storage_service_type.get(),
        LOCAL_FILE_STORAGE_DIR=os.path.join(os.getcwd(), "storage_test"),
        BUCKETS=os.getenv("BUCKETS"),
    )


@pytest.fixture(scope="module", params=TEST_TARGETS)
def client(request):
    file_storage_service_type.set(request.param)
    app.dependency_overrides[get_settings] = get_settings_override  # type: ignore
    # asyncio.run(store._init_buckets())
    with TestClient(app) as client:
        yield client
    shutil.rmtree(os.path.join(os.getcwd(), "storage_test"), ignore_errors=True)
