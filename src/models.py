from datetime import datetime
from peewee_migrate import Router

from src.config import DB_FILENAME, MIGRATIONS_DIR
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
    user = ForeignKeyField(User)


def init_db():
    router = Router(db, migrate_dir=MIGRATIONS_DIR)
    with db:
        router.run()
