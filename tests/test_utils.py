import pytest

from unittest import mock

from src.utils import get_password_hash
# from tests.conftest import init_test_db


@pytest.mark.parametrize("password, salt, result", [
    ("admin", "", "8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918"),
    ("admin", "salt", "2bb7998496899acdd8137fad3a44faf96a84a03d7f230ce42e97cd17c7ae429e"),
    ("qwerty", "", "65e84be33532fb784c48129675f9eff3a682b27168c0ea744b2cf58ee02337c5"),
    ("qwerty", "salt", "c486321c1f7a6decc05ff38c89fe4ce0bf6816e3cd9f013347a538b5fdf05e53"),
])
def test_get_password_hash(password, salt, result):
    with mock.patch("src.utils.secret_key", salt):
        assert get_password_hash(password) == result
