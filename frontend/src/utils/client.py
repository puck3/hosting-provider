import requests
import streamlit as st
from src.core.config import BACKEND_URL


class Client:
    def __init__(self):
        self.base_url = BACKEND_URL.rstrip("/")
        self.login_url = f"{self.base_url}/auth/login"
        self.refresh_url = f"{self.base_url}/auth/refresh"

    def login(self, username: str, password: str) -> None:
        response = requests.post(
            self.login_url,
            data={"username": username, "password": password},
        )
        response.raise_for_status()

        tokens = response.json()
        self._store_tokens(tokens)

    def request(self, method: str, endpoint: str, **kwargs) -> dict | list:
        response = self._get_response(method, endpoint, **kwargs)
        response.raise_for_status()
        return response.json()

    def protected_request(self, method: str, endpoint: str, **kwargs) -> dict | list:
        headers = kwargs.pop("headers", {})
        headers.update(self._get_auth_headers())
        response = self._get_response(method, endpoint, headers=headers, **kwargs)
        if response.status_code == 401:
            self._refresh_tokens()
            headers = self._get_auth_headers()
            response = self._get_response(method, endpoint, headers=headers, **kwargs)

        response.raise_for_status()
        return response.json()

    def refresh_request(self, method: str, endpoint: str, **kwargs) -> None:
        headers = kwargs.pop("headers", {})
        headers.update(self._get_auth_headers())
        tokens = self.request(method, endpoint, headers=headers, **kwargs)
        assert isinstance(tokens, dict)
        self._store_tokens(tokens)

    def _get_response(self, method: str, endpoint: str, **kwargs) -> requests.Response:
        url = f"{self.base_url}{endpoint}"
        return requests.request(method, url, **kwargs)

    def _get_auth_headers(self) -> dict:
        access_token = st.session_state.get("access_token")
        if not access_token:
            raise ValueError("Access token not found")

        return {"Authorization": f"Bearer {access_token}"}

    def _get_refresh_headers(self) -> dict:
        refresh_token = st.session_state.get("refresh_token")
        if not refresh_token:
            raise ValueError("Refreshtoken not found")

        return {"Authorization": f"Bearer {refresh_token}"}

    def _refresh_tokens(self) -> None:
        refresh_token = st.session_state.get("refresh_token")
        if not refresh_token:
            raise ValueError("No refresh token available")

        response = requests.get(
            self.refresh_url,
            data={"refresh_token": refresh_token},
        )
        response.raise_for_status()
        tokens = response.json()
        self._store_tokens(tokens)

    def _store_tokens(self, tokens: dict) -> None:
        st.session_state["access_token"] = tokens["access_token"]
        st.session_state["refresh_token"] = tokens["refresh_token"]

    def logout(self) -> None:
        st.session_state.pop("access_token", None)
        st.session_state.pop("refresh_token", None)
        st.session_state.pop("user_id", None)
        st.session_state.pop("role", None)
