from typing import Optional

from fastapi import APIRouter

from src.exceptions import BadRequestException
from src.models import User
from src.utils import open_connection, get_password_hash
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
):
    """
    :return: all notes related to user (by id).\n
    If id is not set, returns all existed notes.\n
    `limit` and `offset` - standard SQL query parameters.
    """
    query = User.select(User.id, User.username, User.created_at).dicts()
    query = query.limit(limit) if limit else query
    query = query.offset(offset) if offset else query
    return {"users": list(query)}


@router.post("/")
@open_connection
async def create_user(item: TypeUserCreate):
    result = User.create(
        username=item.username,
        password=get_password_hash(item.password)
    )
    return {"result": result}


@router.put("/{user_id}")
@open_connection
async def update_user(*, user_id: int = notations["p_user_id"], item: TypeUserUpdate):
    if not (item.password or item.username):
        raise BadRequestException("Either `password` or `user_id` parameter is empty.")

    params = {}
    if item.password:
        params["password"] = get_password_hash(item.password)
    if item.username:
        params["username"] = item.username
    result = User.update(**params).where(User.id == user_id).execute()
    return {"result": result}


@router.delete("/{user_id}")
@open_connection
async def delete_user(user_id: int = notations["p_user_id"]):
    result = User.delete().where(User.id == user_id).execute()
    return {"result": result}
