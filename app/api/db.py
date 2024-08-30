from sqlalchemy import (
    Column,
    Integer,
    MetaData,
    String,
    Table,
    create_engine,
    ForeignKey,
)
from databases import Database
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
metadata = MetaData()

notes = Table(
    "notes",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("text", String(250)),
    Column("user_id", Integer, ForeignKey("users.id")),
)

users = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("username", String, unique=True, nullable=False),
    Column("password", String, nullable=False),
)

database = Database(DATABASE_URL)
