from pydantic import BaseModel
from typing import Optional


class NoteCreate(BaseModel):
    text: str
    user_id: Optional[int] = None


class NoteUpdate(BaseModel):
    text: Optional[str] = None
    user_id: Optional[int] = None


class UserCreate(BaseModel):
    username: str
    password: str


class UserUpdate(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None
