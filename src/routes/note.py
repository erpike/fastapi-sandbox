from typing import Optional

from fastapi import APIRouter, Response
from playhouse.shortcuts import model_to_dict
from starlette import status

from src.models import Note
from src.type_models import (
    NoteCreate as TypeNoteCreate,
    NoteUpdate as TypeNoteUpdate,
)
from src.utils import open_connection
from src.vars import notations


router = APIRouter(prefix="/note", tags=["Note"])


@router.get(
    "{note_id}",
    status_code=status.HTTP_200_OK,
    summary="Get note by id.",
    description="Get note by id.<br>`id` param value should be more that 0."
)
@open_connection
async def get_note(response: Response, note_id: int = notations["note_id"]):
    # No validation required as FastAPI already done this job :)
    # if not note_id or type(note_id) is not int:
    #     return {"error": "Invalid `note_id` parameter"}
    note = Note.get_or_none(id=note_id)
    if not note:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"error": "Not found"}
    return {"note": note and model_to_dict(note, recurse=False)}


@router.get("/", response_description="List of notes")
@open_connection
async def list_note(
    limit: Optional[int] = notations["limit"],
    offset: Optional[int] = notations["offset"],
    user_id: Optional[int] = notations["q_user_id"],
):
    """
    :return: all notes related to user (by id).\n
    If id is not set, returns all existed notes.\n
    `limit` and `offset` - standard SQL query parameters.
    """
    query = Note.select().dicts()
    query = query.where(Note.user_id == user_id) if user_id else query
    query = query.limit(limit) if limit else query
    query = query.offset(offset) if offset else query
    return {"notes": list(query)}


@router.post("/")
@open_connection
async def create_note(item: TypeNoteCreate):
    result = Note.create(
        text=item.text,
        user=item.user_id or None,
    )
    return {"result": result}


@router.put("/{note_id}")
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


@router.delete("/")
@open_connection
async def delete_note(note_id: int = notations["limit"]):
    result = Note.delete().where(Note.id == note_id).execute()
    return {"result": result}
