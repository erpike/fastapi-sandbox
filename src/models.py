from datetime import datetime
from peewee_migrate import Router

from src.config import (
    DB_FILENAME,
    MIGRATIONS_DIR,
    superuser_name,
    superuser_password,
)
from peewee import (
    CharField,
    DateTimeField,
    ForeignKeyField,
    Model,
    SqliteDatabase,
    TextField,
)


db = SqliteDatabase(
    DB_FILENAME,
    autoconnect=False,
    pragmas={"foreign_keys": 1}
)


class BaseModel(Model):
    class Meta:
        database = db

    created_at = DateTimeField(default=datetime.utcnow)


class User(BaseModel):
    username = CharField(max_length=255, unique=True, null=False)
    password = CharField(max_length=255, null=False)


class Note(BaseModel):
    text = TextField(null=False)
    user = ForeignKeyField(User, on_delete="CASCADE", null=True)


def create_superuser():
    if not (superuser_name and superuser_password):
        raise Exception(
            "Insufficient credentials for superuser. "
            "Please, provide environment variables `USER_NAME` and `USER_PASSWORD`"
        )
    try:
        from src.utils import get_password_hash
        User.get_or_create(
            username=superuser_name,
            password=get_password_hash(superuser_password),
        )
    except Exception: # noqa
        raise Exception("Can't create superuser.")


def init_db():
    router = Router(db, migrate_dir=MIGRATIONS_DIR)
    with db:
        router.run()
        create_superuser()
