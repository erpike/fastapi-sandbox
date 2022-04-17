from datetime import datetime
from peewee_migrate import Router

from src.conf import DB_FILENAME, MIGRATIONS_DIR
from peewee import (
    DateTimeField,
    Model,
    SqliteDatabase,
    TextField,
)


db = SqliteDatabase(DB_FILENAME, autoconnect=False)


class BaseModel(Model):
    class Meta:
        database = db

    created_at = DateTimeField(default=datetime.utcnow)


class Note(BaseModel):
    text = TextField()


def init_db():
    router = Router(db, migrate_dir=MIGRATIONS_DIR)
    with db:
        router.run()
