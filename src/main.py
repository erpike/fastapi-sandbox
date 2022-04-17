from fastapi import FastAPI
from playhouse.shortcuts import model_to_dict

from src.models import (
    db,
    init_db,
    Note,
)


app = FastAPI(title="Awesome Fast API Sandbox.")


@app.on_event("startup")
async def on_startup():
    init_db()


@app.get("/note/{note_id}")
async def get_note(note_id: int):
    if not note_id or type(note_id) is not int:
        return {"error": "Invalid `note_id` parameter"}
    with db:
        note = Note.get_or_none(id=note_id)
        return {"note": note and model_to_dict(note)}


@app.get("/note/")
async def list_note(limit=None, offset=None):
    with db:
        query = Note.select().dicts()
        query = query.limit(limit) if limit else query
        query = query.offset(offset) if offset else query
        return {"notes": list(query)}


@app.post("/note/")
async def create_note(text):
    with db:
        Note.create(text=text)


@app.delete("/note/")
async def delete_note(note_id: int):
    with db:
        result = Note.delete().where(Note.id == note_id).execute()
    return {"result": result}
