import hashlib
from functools import wraps
from peewee import IntegrityError

from src.conf import SECRET_KEY
from src.models import db


def open_connection(coro):
    @wraps(coro)
    async def wrapper(*args, **kwargs):
        try:
            with db:
                return await coro(*args, **kwargs)
        except IntegrityError:
            return {"error": "IntegrityError during query."}
    return wrapper


# TODO: fix import error. Can't run python src/utils.py from root.
def get_password_hash(password: str):
    return hashlib.sha256(f"{SECRET_KEY}{password}".encode("utf8")).hexdigest()
