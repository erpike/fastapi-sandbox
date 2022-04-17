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
from src.type_models import Note as TypeNote
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
    return {"note": note and model_to_dict(note)}


@app.get("/note/")
@open_connection
async def list_note(
    limit: Optional[int] = notations["limit"],
    offset: Optional[int] = notations["offset"],
    user_id: Optional[int] = notations["user_id"],
):
    query = Note.select().dicts()
    query = query.where(Note.user_id == user_id) if user_id else query
    query = query.limit(limit) if limit else query
    query = query.offset(offset) if offset else query
    return {"notes": list(query)}


@app.post("/note/")
@open_connection
async def create_note(item: TypeNote):
    Note.create(
        text=item.text,
        user=item.user_id or None,
    )


@app.put("/note/{note_id}")
@open_connection
async def update_note(*, note_id: int = notations["note_id"], item: TypeNote):
    params = {}
    if item.text:
        params["text"] = item.text
    if item.user_id:
        params["user_id"] = item.user_id
    Note.update(**params).where(Note.id == note_id).execute()


@app.delete("/note/")
@open_connection
async def delete_note(note_id: int = notations["limit"]):
    result = Note.delete().where(Note.id == note_id).execute()
    return {"result": result}


@app.post("/user/{username}")
@open_connection
async def create_user(username: str = notations["username"]):
    User.create(username=username)
