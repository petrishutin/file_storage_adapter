import os
import uuid
from http import HTTPStatus


def test_upload_201(client):
    """response status is OK and body contains correct cropped image"""
    with open("tests/assets/cat.jpg", "rb") as f:
        file_data = f.read()
    response = client.post("/", files={"file": file_data})
    assert response.status_code == HTTPStatus.CREATED
    assert uuid.UUID(response.json())
    client.delete("/", params={"file_name": response.json()})


def test_download_200(client):
    """response status is OK and body contains correct cropped image"""
    with open("tests/assets/cat.jpg", "rb") as f:
        file_data = f.read()
    response = client.post("/", files={"file": file_data})
    file_name = response.json()
    response = client.get("/", params={"file_name": file_name})
    assert response.status_code == HTTPStatus.OK
    assert response.content == file_data
    client.delete("/", params={"file_name": file_name})


def test_delete_204(client):
    print(os.getenv("BUCKETS"))
    """response status is OK and body contains correct cropped image"""
    with open("tests/assets/cat.jpg", "rb") as f:
        file_data = f.read()
    response = client.post("/", files={"file": file_data})
    file_name = response.json()
    response = client.delete("/", params={"file_name": str(file_name)})
    assert response.status_code == HTTPStatus.NO_CONTENT
