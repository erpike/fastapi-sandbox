import os

import pytest

from fastapi.testclient import TestClient
from peewee import SqliteDatabase

from main import app
from src.auth.oauth2 import identify_user
from src.models import MODELS, db_proxy

test_db = SqliteDatabase(
    "test.db",
    pragmas={"foreign_keys": 1},
)


@pytest.fixture
def client_authenticated():
    def skip_auth():
        pass

    app.dependency_overrides[identify_user] = skip_auth
    return TestClient(app)


@pytest.fixture(scope="function", autouse=True)
def init_test_db():
    with db_proxy:
        db_proxy.drop_tables(MODELS)
        db_proxy.create_tables(MODELS)


@pytest.fixture(scope="session", autouse=True)
def manage_db():
    db_proxy.initialize(test_db)
    yield
    os.remove("test.db") if os.path.exists("test.db") else None
