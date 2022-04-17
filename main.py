from typing import Optional

from fastapi import FastAPI
from functools import wraps

from peewee import IntegrityError
from playhouse.shortcuts import model_to_dict


from src.models import (
    db,
    init_db,
    Note,
    User,
)
from src.type_models import (
    NoteCreate as TypeNoteCreate,
    NoteUpdate as TypeNoteUpdate,
    UserCreate as TypeUserCreate,
    UserUpdate as TypeUserUpdate,
)
from src.utils import get_password_hash
from src.vars import notations


app = FastAPI(title="Awesome Fast API Sandbox.")


def open_connection(coro):
    @wraps(coro)
    async def wrapper(*args, **kwargs):
        try:
            with db:
                return await coro(*args, **kwargs)
        except IntegrityError:
            return {"error": "IntegrityError during query."}
    return wrapper


@app.on_event("startup")
async def on_startup():
    init_db()


@app.get("/note/{note_id}")
@open_connection
async def get_note(note_id: int = notations["note_id"]):
    # No validation required as FastAPI already done this job :)
    # if not note_id or type(note_id) is not int:
    #     return {"error": "Invalid `note_id` parameter"}
    note = Note.get_or_none(id=note_id)
    return {"note": note and model_to_dict(note, recurse=False)}


@app.get("/note/")
@open_connection
async def list_note(
    limit: Optional[int] = notations["limit"],
    offset: Optional[int] = notations["offset"],
    user_id: Optional[int] = notations["q_user_id"],
):
    query = Note.select().dicts()
    query = query.where(Note.user_id == user_id) if user_id else query
    query = query.limit(limit) if limit else query
    query = query.offset(offset) if offset else query
    return {"notes": list(query)}


@app.post("/note/")
@open_connection
async def create_note(item: TypeNoteCreate):
    result = Note.create(
        text=item.text,
        user=item.user_id or None,
    )
    return {"result": result}


@app.put("/note/{note_id}")
@open_connection
async def update_note(*, note_id: int = notations["note_id"], item: TypeNoteUpdate):
    if not item.text or not item.user_id:
        return {"error": "Invalid request parameters."}

    params = {}
    if item.text:
        params["text"] = item.text
    if item.user_id:
        params["user_id"] = item.user_id
    result = Note.update(**params).where(Note.id == note_id).execute()
    return {"result": result}


@app.delete("/note/")
@open_connection
async def delete_note(note_id: int = notations["limit"]):
    result = Note.delete().where(Note.id == note_id).execute()
    return {"result": result}


@app.post("/user/{username}")
@open_connection
async def create_user(item: TypeUserCreate):
    result = User.create(
        username=item.username,
        password=get_password_hash(item.password)
    )
    return {"result": result}


@app.put("/user/{user_id}")
@open_connection
async def update_user(*, user_id: int = notations["p_user_id"], item: TypeUserUpdate):
    if not item.password or not item.username:
        return {"error": "Invalid request parameters."}

    params = {}
    if item.password:
        params["password"] = get_password_hash(item.password)
    if item.username:
        params["username"] = item.username
    result = User.update(**params).where(User.id == user_id).execute()
    return {"result": result}
