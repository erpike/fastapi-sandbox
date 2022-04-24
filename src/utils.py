import datetime
import hashlib

from functools import wraps
from json import JSONEncoder

from peewee import IntegrityError

from src.config import secret_key
from src.exceptions import DBException
from src.models import db, db_proxy


class DateTimeEncoder(JSONEncoder):
    # Override the default method
    def default(self, obj):
        if isinstance(obj, (datetime.date, datetime.datetime)):
            return obj.isoformat()


def open_connection(coro):
    @wraps(coro)
    async def wrapper(*args, **kwargs):
        try:
            with db_proxy:
                return await coro(*args, **kwargs)
        except IntegrityError as e:
            raise DBException(f"DB ERROR: {e}")
    return wrapper


# TODO: fix import error. Can't run python src/utils.py from root.
def get_password_hash(password: str):
    return hashlib.sha256(f"{secret_key}{password}".encode("utf8")).hexdigest()
