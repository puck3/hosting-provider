import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.db.connector import initialize_connection, close_connection_pool


@pytest.fixture(scope="module")
def client():
    initialize_connection()
    yield TestClient(app)
    close_connection_pool()
