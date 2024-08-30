import fastapi

from app.api.db import database, users
from fastapi.security import HTTPBasic, HTTPBasicCredentials

# Аутентификация и авторизация
security = HTTPBasic()


# Функция получения текущего пользователя
async def get_current_user(credentials: HTTPBasicCredentials = fastapi.Depends(security)):
    username = credentials.username
    # Ищем пользователя в базе данных
    user = await database.fetch_one(users.select().where(users.c.username == username))
    if user is None:
        raise fastapi.HTTPException(status_code=400, detail="User not found")
    return user
