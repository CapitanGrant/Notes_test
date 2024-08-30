from pydantic import BaseModel
from typing import Optional


# Объявление модели Pydantic
class NoteIn(BaseModel):
    text: str


class NoteOut(NoteIn):
    id: int
    user_id: int


class NoteUpdate(BaseModel):
    text: Optional[str] = None
