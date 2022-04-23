from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status

from src.auth.oauth2 import create_access_token
from src.models import User
from src.utils import open_connection, get_password_hash


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post("/token")  # the same as OAuth2PasswordBearer.tokenUrl param
@open_connection
async def get_token(request: OAuth2PasswordRequestForm = Depends()):
    user = User.get_or_none(username=request.username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid credentials",
        )
    if get_password_hash(request.password) != user.password:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Incorrect password"
        )
    access_token = create_access_token(data=dict(sub=user.username))
    return {
        "access_token": access_token,
        "token_type": "Bearer",
        "user_id": user.id,
    }
