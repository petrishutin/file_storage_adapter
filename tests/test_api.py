import uuid
from http import HTTPStatus


def test_upload_201(client):
    """response status is OK and body contains correct cropped image"""
    file_data = "test"
    response = client.post("/", data={"file": file_data})
    assert response.status_code == HTTPStatus.CREATED
    assert uuid.UUID(response.json())
    client.delete("/", params={"file_name": response.json()})


def test_download_200(client):
    """response status is OK and body contains correct cropped image"""
    file_data = "test"
    response = client.post("/", data={"file": file_data})
    file_name = response.json()
    response = client.get("/", params={"file_name": str(file_name)})
    assert response.status_code == HTTPStatus.OK
    assert response.content == b"test"
    client.delete("/", params={"file_name": str(file_name)})


def test_delete_204(client):
    """response status is OK and body contains correct cropped image"""
    file_data = "test"
    response = client.post("/", data={"file": file_data})
    file_name = response.json()
    response = client.delete("/", params={"file_name": str(file_name)})
    assert response.status_code == HTTPStatus.NO_CONTENT
