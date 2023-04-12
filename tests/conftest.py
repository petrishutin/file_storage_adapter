import os
import shutil
from os.path import join
from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.settings import Settings


@pytest.fixture(scope="module")
def bytes_cropped_image():
    with open("tests/assets/cropped/cropped_dog.jpeg", "rb") as f:
        return f.read()


@pytest.fixture(
    scope="session",
    params=["LocalFileStorage", "S3FileStorage"],
)
def client(request):
    test_settings = Settings(
        FILE_STORAGE_SERVICE=request.param,
        LOCAL_FILE_STORAGE_DIR=join(os.getcwd(), "storage_test"),
    )
    with patch("app.settings.settings", test_settings):
        with TestClient(app) as client:
            yield client
        shutil.rmtree(join(os.getcwd(), "storage_test"), ignore_errors=True)
