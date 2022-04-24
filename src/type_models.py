from pydantic import BaseModel, constr
from typing import Optional


class NoteCreate(BaseModel):
    text: str
    user_id: Optional[int] = None


class NoteUpdate(BaseModel):
    text: Optional[str] = None
    user_id: Optional[int] = None


class UserCreate(BaseModel):
    username: constr(min_length=2)
    password: constr(min_length=5)


class UserUpdate(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None
