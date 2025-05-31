from datetime import date

from src.models.user import Role, User
from src.utils.client import Client


class UserService:
    def __init__(self, client: Client) -> None:
        self.client = client

    def get_self(self) -> User:
        response = self.client.protected_request("GET", "/users/self")
        user = User.model_validate(response)
        return user

    def get_users(self) -> list[User]:
        response = self.client.protected_request("GET", "/users")
        return [User.model_validate(user) for user in response]

    def get_user_by_id(self, user_id: int) -> User | None:
        response = self.client.protected_request("GET", f"/users/{user_id}")
        return User.model_validate(response)

    def delete_user(self, user_id: int, password: str) -> None:
        self.client.protected_request("DELETE", f"/users/{user_id}", json={"password": password})

    def create_user(
        self,
        email: str,
        login: str,
        password: str,
        first_name: str | None = None,
        last_name: str | None = None,
        birthdate: date | None = None,
    ) -> User:
        body = {
            "email": email,
            "login": login,
            "password": password,
            "first_name": first_name,
            "last_name": last_name,
            "birthdate": birthdate,
        }
        response = self.client.request("POST", "/users", json=body)
        user = User.model_validate(response)
        return user

    def change_user_personal(
        self,
        user_id: int,
        first_name: str | None = None,
        last_name: str | None = None,
        birthdate: date | None = None,
    ) -> None:
        body = {
            "first_name": first_name,
            "last_name": last_name,
            "birthdate": birthdate,
        }
        self.client.protected_request("PATCH", f"/users/{user_id}", json=body)

    def change_user_role_by_email(self, email: str, role: Role) -> None:
        body = {"role": role.value}
        self.client.protected_request("PATCH", f"/users/role/{email}", json=body)

    def change_user_password(self, old_password: str, new_password: str) -> None:
        body = {"old_password": old_password, "new_password": new_password}
        self.client.refresh_request("PATCH", "/auth/refresh/password", json=body)

    def change_user_email(self, password: str, email: str) -> None:
        body = {"password": password, "email": email}
        self.client.refresh_request("PATCH", "/auth/refresh/email", json=body)

    def change_user_login(self, password: str, login: str) -> None:
        body = {"password": password, "login": login}
        self.client.refresh_request("PATCH", "/auth/refresh/login", json=body)
