from datetime import timedelta, datetime

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from typing import Optional

from starlette import status

from src.config import ACCESS_TOKEN_EXPIRE_MINUTES, secret_key, ENCODE_ALGORITHM
from src.models import db, User, db_proxy

oauth2_schema = OAuth2PasswordBearer(tokenUrl="/auth/token")


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expires_delta = expires_delta if expires_delta else timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    expires = datetime.utcnow() + expires_delta
    to_encode.update({"expired_at": str(expires)})
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=ENCODE_ALGORITHM)
    return encoded_jwt


def identify_user(token: str = Depends(oauth2_schema)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, secret_key, algorithms=[ENCODE_ALGORITHM])
        username = payload.get("sub")
        if not username:
            raise credentials_exception
        with db_proxy:
            user = User.get_or_none(username=username)
            if not user:
                raise credentials_exception
    except JWTError:
        raise credentials_exception
    return user
