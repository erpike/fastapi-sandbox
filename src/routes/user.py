from fastapi import APIRouter

from src.models import User
from src.utils import open_connection, get_password_hash
from src.type_models import (
    UserCreate as TypeUserCreate,
    UserUpdate as TypeUserUpdate,
)
from src.vars import notations


router = APIRouter(prefix="/user", tags=["User"])


@router.post("/{username}")
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
    if not item.password or not item.username:
        return {"error": "Invalid request parameters."}

    params = {}
    if item.password:
        params["password"] = get_password_hash(item.password)
    if item.username:
        params["username"] = item.username
    result = User.update(**params).where(User.id == user_id).execute()
    return {"result": result}
