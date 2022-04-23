import json

from fastapi import APIRouter, Response, Depends
from typing import Optional

from src.auth.oauth2 import identify_user
from src.exceptions import BadRequestException
from src.models import User
from src.utils import open_connection, get_password_hash, DateTimeEncoder
from src.type_models import (
    UserCreate as TypeUserCreate,
    UserUpdate as TypeUserUpdate,
)
from src.vars import notations


router = APIRouter(prefix="/user", tags=["User"])


@router.get("/", response_description="List of users")
@open_connection
async def list_user(
    limit: Optional[int] = notations["limit"],
    offset: Optional[int] = notations["offset"],
    user: User = Depends(identify_user),
):
    """
    :return: all notes related to user (by id).\n
    If id is not set, returns all existed notes.\n
    `limit` and `offset` - standard SQL query parameters.
    """
    query = User.select(User.id, User.username, User.created_at).dicts()
    query = query.limit(limit) if limit else query
    query = query.offset(offset) if offset else query
    return Response(content=json.dumps(list(query.dicts()), cls=DateTimeEncoder), media_type="application/json")


@router.post("/")
@open_connection
async def create_user(
    item: TypeUserCreate,
    user: User = Depends(identify_user),
):
    result = User.create(
        username=item.username,
        password=get_password_hash(item.password)
    )
    return Response(content=json.dumps({"created": result.id}), media_type="application/json")


@router.put("/{user_id}")
@open_connection
async def update_user(
    *,
    user_id: int = notations["p_user_id"],
    item: TypeUserUpdate,
    user: User = Depends(identify_user),
):
    if not (item.password or item.username):
        raise BadRequestException("Either `password` or `user_id` parameter is empty.")

    params = {}
    if item.password:
        params["password"] = get_password_hash(item.password)
    if item.username:
        params["username"] = item.username
    result = User.update(**params).where(User.id == user_id).execute()
    return Response(content=json.dumps({"updated": result}), media_type="application/json")


@router.delete("/{user_id}")
@open_connection
async def delete_user(
    user_id: int = notations["p_user_id"],
    user: User = Depends(identify_user),
):
    result = User.delete().where(User.id == user_id).execute()
    return Response(content=json.dumps({"deleted": result}), media_type="application/json")
