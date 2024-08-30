from app.api.models import NoteIn, NoteUpdate
from app.api.db import notes, database


async def get_all_notes(user_id: int):
    query = notes.select().where(notes.c.user_id == user_id)
    return await database.fetch_all(query=query)


async def get_note(id: int, user_id: int):
    query = notes.select().where(notes.c.id == id).where(notes.c.user_id == user_id)
    return await database.fetch_one(query=query)


async def delete_note(id: int, user_id: int):
    query = notes.delete().where(notes.c.id == id).where(notes.c.user_id == user_id)
    return await database.execute(query=query)


async def create_note(payload: NoteIn, user_id: int):
    query = notes.insert().values(**payload.dict(), user_id=user_id)
    return await database.execute(query=query)


async def update_note(id: int, payload: NoteUpdate, user_id: int):
    query = (
        notes.update()
        .where(notes.c.id == id)
        .where(notes.c.user_id == user_id)
        .values(**payload.dict())
    )
    return await database.execute(query=query)
