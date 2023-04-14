import os
import shutil
from os.path import join

import pytest
from fastapi.testclient import TestClient


@pytest.fixture(scope="module", params=["LocalFileStorage", "S3FileStorage"], autouse=True)
def client(request):
    os.environ["FILE_STORAGE_SERVICE"] = request.param
    os.environ["LOCAL_FILE_STORAGE_DIR"] = "storage_test"
    from app.main import app

    with TestClient(app) as client:
        yield client
    shutil.rmtree(join(os.getcwd(), "storage_test"), ignore_errors=True)
