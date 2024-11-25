from fastapi import APIRouter, Depends
from src.db.connection import get_connection
import asyncpg

router = APIRouter()


@router.get("/users/")
async def get_users(conn: asyncpg.Connection = Depends(get_connection)):
    query = "SELECT * FROM users"
    return await conn.fetch(query)
