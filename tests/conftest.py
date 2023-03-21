import contextvars
import os
import shutil
from os.path import join

import pytest
from fastapi.testclient import TestClient

from app.main import app, get_settings
from app.settings import Settings


@pytest.fixture(scope="module")
def bytes_cropped_image():
    with open("tests/assets/cropped/cropped_dog.jpeg", "rb") as f:
        return f.read()


file_storage_service_type: contextvars.ContextVar = contextvars.ContextVar("LocalFileStorage")


def get_settings_override():
    return Settings(
        FILE_STORAGE_SERVICE=file_storage_service_type.get(),
        LOCAL_FILE_STORAGE_DIR=join(os.getcwd(), "storage_test"),
    )


@pytest.fixture(
    scope="session",
    params=["LocalFileStorage", "S3FileStorage"],
)
def client(request):
    file_storage_service_type.set(request.param)
    app.dependency_overrides[get_settings] = get_settings_override  # type: ignore
    with TestClient(app) as client:
        yield client
    shutil.rmtree(join(os.getcwd(), "storage_test"), ignore_errors=True)