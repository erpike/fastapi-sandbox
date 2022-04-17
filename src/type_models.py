from pydantic import BaseModel
from typing import Optional


class Note(BaseModel):
    text: str = ""
    user_id: Optional[int] = None
