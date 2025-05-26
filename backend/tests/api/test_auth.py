from httpx import Response


from fastapi.testclient import TestClient
import pytest
from starlette.status import HTTP_200_OK
from app.api.v1.schemas.user import ChangeEmail, ChangeLogin, ChangePassword
from app.main import app

client = TestClient(app)


@pytest.fixture()
def username():
    return "admin"


@pytest.fixture()
def password():
    return "admin"


@pytest.fixture()
def email():
    return "admin@example.com"


def request_login(client, username: str, password: str) -> Response:
    form_data = {
        "username": username,
        "password": password,
        "grant_type": "password",
    }
    response = client.post(
        "/auth/login",
        data=form_data,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    return response


def test_login(client, username, password):
    response = request_login(client, username, password)
    assert response.status_code == HTTP_200_OK
    assert "access_token" in response.json()
    assert "refresh_token" in response.cookies


def login(client: TestClient, username: str, password: str):
    response = request_login(client, username, password)
    assert response.status_code == HTTP_200_OK
    refresh_token = response.cookies.get("refresh_token")
    assert refresh_token is not None
    client.cookies.set("refresh_token", refresh_token)


def test_refresh(client, username, password):
    login(client, username, password)
    response = client.get("/auth/refresh")

    assert response.status_code == HTTP_200_OK
    assert "access_token" in response.json()
    assert "refresh_token" in response.cookies


def refresh(client: TestClient):
    response = client.get("/auth/refresh")
    assert response.status_code == HTTP_200_OK
    refresh_token = response.cookies.get("refresh_token")
    assert refresh_token is not None
    client.cookies.set("refresh_token", refresh_token)


def request_change_password(
    client: TestClient, old_password: str, new_password: str
) -> Response:
    body = ChangePassword(old_password=old_password, new_password=new_password)
    return client.patch("/auth/refresh/password", json=body.model_dump())


def test_change_user_password(client, password, username):
    new_password = "new_test_password"
    login(client, username, password)
    response = request_change_password(client, password, new_password)
    assert response.status_code == HTTP_200_OK
    assert "access_token" in response.json()
    assert "refresh_token" in response.cookies
    login(client, username, new_password)

    response = request_change_password(client, new_password, password)
    assert response.status_code == HTTP_200_OK
    assert "access_token" in response.json()
    assert "refresh_token" in response.cookies


def request_change_email(
    client: TestClient, password: str, email: str
) -> Response:
    body = ChangeEmail(password=password, email=email)
    return client.patch("/auth/refresh/email", json=body.model_dump())


def test_change_user_email(client, username, password, email):
    new_email = "new_test_email@example.com"
    login(client, username, password)
    response = request_change_email(client, password, new_email)
    assert response.status_code == HTTP_200_OK
    assert "access_token" in response.json()
    assert "refresh_token" in response.cookies

    refresh_token = response.cookies.get("refresh_token")
    client.cookies.set("refresh_token", refresh_token)
    refresh(client)

    response = request_change_email(client, password, email)
    assert response.status_code == HTTP_200_OK
    assert "access_token" in response.json()
    assert "refresh_token" in response.cookies


def request_change_login(
    client: TestClient, password: str, login: str
) -> Response:
    body = ChangeLogin(password=password, login=login)
    return client.patch("/auth/refresh/login", json=body.model_dump())


def test_change_user_login(client, username, password):
    new_login = "new_test_login"
    login(client, username, password)
    response = request_change_login(client, password, new_login)
    assert response.status_code == HTTP_200_OK
    assert "access_token" in response.json()
    assert "refresh_token" in response.cookies

    login(client, new_login, password)

    response = request_change_login(client, password, username)
    assert response.status_code == HTTP_200_OK
    assert "access_token" in response.json()
    assert "refresh_token" in response.cookies
