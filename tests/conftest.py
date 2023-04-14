import os
import shutil
from os.path import join

import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture(
    scope="session",
    params=["LocalFileStorage", "S3FileStorage"],
)
def client(request):
    os.environ["FileStorageService"] = request.param
    os.environ["LocalFileStorageDir"] = "storage_test"
    with TestClient(app) as client:
        yield client
    shutil.rmtree(join(os.getcwd(), "storage_test"), ignore_errors=True)
