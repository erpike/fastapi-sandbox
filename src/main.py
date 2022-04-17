from typing import Optional

from fastapi import FastAPI
from functools import wraps
from playhouse.shortcuts import model_to_dict

from src.models import (
    db,
    init_db,
    Note,
)
from src.vars import notations


app = FastAPI(title="Awesome Fast API Sandbox.")


def open_connection(coro):
    @wraps(coro)
    async def wrapper(*args, **kwargs):
        with db:
            return await coro(*args, **kwargs)
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
async def list_note(limit: int = notations["limit"], offset: int = notations["offset"]):
    query = Note.select().dicts()
    query = query.limit(limit) if limit else query
    query = query.offset(offset) if offset else query
    return {"notes": list(query)}


@app.post("/note/")
@open_connection
async def create_note(text):
    Note.create(text=text)


@app.delete("/note/")
@open_connection
async def delete_note(note_id: int = notations["limit"]):
    result = Note.delete().where(Note.id == note_id).execute()
    return {"result": result}
