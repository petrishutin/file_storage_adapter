import uuid
from http import HTTPStatus

import pytest


def test_upload(client):
    """response status is OK and body contains correct cropped image"""
    file_data = "test"
    response = client.post("/", data={"file": file_data})
    assert response.status_code == HTTPStatus.CREATED
    assert uuid.UUID(response.json())


def test_download(client):
    """response status is OK and body contains correct cropped image"""
    file_data = "test"
    response = client.post("/", data={"file": file_data})
    file_name = response.json()
    response = client.get("/", params={"file_name": str(file_name)})
    assert response.status_code == HTTPStatus.OK
    assert response.content == b"test"
