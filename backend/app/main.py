from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from uvicorn import run

from app.api.v1.endpoints import router as router_v1
from app.db.connector import close_connection_pool, initialize_connection


@asynccontextmanager
async def lifespan(app: FastAPI):
    initialize_connection()
    yield
    close_connection_pool()


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(router_v1)


def main():
    run("app.main:app", host="0.0.0.0", port=8000, reload=True)
