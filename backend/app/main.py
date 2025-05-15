from contextlib import asynccontextmanager
from fastapi import FastAPI
from uvicorn import run

from app.api.v1.endpoints import router as router_v1
from app.db.connector import initialize_services_factory, close_connection_pool


@asynccontextmanager
async def lifespan(app: FastAPI):
    initialize_services_factory()
    yield
    close_connection_pool()


app = FastAPI(lifespan=lifespan)
app.include_router(router_v1)


def main():
    run("app.main:app", host="0.0.0.0", port=8000, reload=True)
