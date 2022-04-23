import json
from typing import Optional, List

from fastapi import APIRouter, Header, Response, Depends
from playhouse.shortcuts import model_to_dict
from starlette import status

from src.auth.oauth2 import oauth2_schema
from src.exceptions import BadRequestException
from src.models import Note
from src.type_models import (
    NoteCreate as TypeNoteCreate,
    NoteUpdate as TypeNoteUpdate,
)
from src.utils import open_connection, DateTimeEncoder
from src.vars import notations


router = APIRouter(prefix="/note", tags=["Note"])


@router.get(
    "{note_id}",
    status_code=status.HTTP_200_OK,
    summary="Get note by id.",
    description="Get note by id.<br>`id` param value should be more that 0."
)
@open_connection
async def get_note(
    note_id: int = notations["note_id"],
    query_note_id=notations["q_note_id"],
    custom_header: Optional[List[str]] = Header(None),
    token: str = Depends(oauth2_schema),
):
    # No validation required as FastAPI already done this job :)
    # if not note_id or type(note_id) is not int:
    #     return {"error": "Invalid `note_id` parameter"}
    note = Note.get_or_none(id=note_id)
    if not note:
        return Response(
            status_code=status.HTTP_404_NOT_FOUND,
            content=json.dumps({"error": "Not found"}),
            media_type="application/json",
        )
    m2d = model_to_dict(note, recurse=False)
    response_headers = {
        "request-headers": str(custom_header),
    }
    return Response(
        headers=response_headers,
        content=json.dumps(m2d, cls=DateTimeEncoder),
        media_type="application/json",
    )


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
    return Response(content=json.dumps(list(query.dicts()), cls=DateTimeEncoder), media_type="application/json")


@router.post("/")
@open_connection
async def create_note(item: TypeNoteCreate):
    result = Note.create(
        text=item.text,
        user=item.user_id or None,
    )
    return Response(content=json.dumps({"created": result.id}), media_type="application/json")


@router.put("/{note_id}")
@open_connection
async def update_note(*, note_id: int = notations["note_id"], item: TypeNoteUpdate):
    if not item.text and not item.user_id:
        raise BadRequestException("Either `text` or `user_id` parameter is empty.")

    params = {}
    if item.text:
        params["text"] = item.text
    if item.user_id:
        params["user_id"] = item.user_id
    result = Note.update(**params).where(Note.id == note_id).execute()
    return Response(content=json.dumps({"updated": result}), media_type="application/json")


@router.delete("/{note_id}")
@open_connection
async def delete_note(note_id: int = notations["note_id"]):
    result = Note.delete().where(Note.id == note_id).execute()
    return Response(content=json.dumps({"deleted": result}), media_type="application/json")
