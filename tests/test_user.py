from src.models import User
from tests.conftest import client_authenticated


def test_list_user(client_authenticated):
    User.create(username="user 1", password="pass1", created_at="2020-02-02")
    User.create(username="user 2", password="pass2", created_at="2020-02-02")
    response = client_authenticated.get("/user/")
    assert response.status_code == 200
    assert response.json() == [
        {"id": 1, "username": "user 1", "created_at": "2020-02-02T00:00:00"},
        {"id": 2, "username": "user 2", "created_at": "2020-02-02T00:00:00"},
    ]


def test_create_user(client_authenticated):
    json = {"username": "admin", "password": "admin"}
    response = client_authenticated.post("/user/", json=json)
    assert response.status_code == 200
    assert User.select().count() == 1
