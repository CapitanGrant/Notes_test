import fastapi
from typing import List
from fastapi import APIRouter
from sqlalchemy.testing.pickleable import User
import httpx
from app.api.authenticate import get_current_user
from app.api.models import NoteIn, NoteOut, NoteUpdate
from app.api import db_manager

notes = APIRouter()


async def check_spelling(text: str) -> bool:
    url = "https://speller.yandex.net/services/spellservice.json/checkText"
    params = {"text": text}
    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)
        response_data = response.json()
        print(response_data)
        return len(response_data) == 0  # Если ошибок нет, возвращаем True


# Конечные точки API
@notes.get("/notes/", response_model=List[NoteOut])
async def index(current_user: User = fastapi.Depends(get_current_user)):
    return await db_manager.get_all_notes(current_user.id)


@notes.get("/notes/{id}/", response_model=NoteOut)
async def get_note(id: int, current_user: User = fastapi.Depends(get_current_user)):
    note = await db_manager.get_note(id, current_user.id)
    return note


@notes.post("/notes/", response_model=NoteOut)
async def create_note(note: NoteIn, current_user: User = fastapi.Depends(get_current_user)):
    note_id = await db_manager.create_note(note, current_user.id)
    if not await check_spelling(note.text):
        raise fastapi.HTTPException(status_code=400, detail="Исправьте орфографические ошибки")
    return NoteOut(id=note_id, text=note.text, user_id=current_user.id)


@notes.put("/notes/{id}/", response_model=NoteOut)
async def update_note(
        id: int, note: NoteUpdate, current_user: User = fastapi.Depends(get_current_user)
):
    updated_note = await db_manager.update_note(id, note, current_user.id)
    return NoteOut(id=updated_note, text=note.text, user_id=current_user.id)


@notes.delete("/notes/{id}/", response_model=dict)
async def delete_note(id: int, current_user: User = fastapi.Depends(get_current_user)):
    deleted = await db_manager.delete_note(id, current_user.id)
    return {"status": "success"}
