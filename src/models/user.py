from src.schemas.user import default_str, email_str, Role, Personal
from src.core.config import password_context


class User:
    def __init__(
        self,
        email: email_str,
        login: default_str,
        password: str,
        hashed: bool = False,
        role: Role = Role.user,
        personal: Personal | None = None,
        user_id: int | None = None,
    ) -> None:
        self.email = email
        self.login = login
        self.hashed_password = password if hashed else password_context.hash(password)
        self.role = role
        self.personal = personal
        self.user_id = user_id

    def check_password(self, password: str) -> bool:
        return password_context.verify(password, self.hashed_password)

    def set_password(self, old_password: str, new_password: str):
        if self.check_password(old_password):
            self.hashed_password = password_context.hash(new_password)
            return True
        return False

    def set_email(self, password: str, new_email: email_str) -> bool:
        if self.check_password(password):
            self._email = new_email
            return True
        return False

    def set_login(self, password: str, new_login: default_str) -> bool:
        if self.check_password(password):
            self._login = new_login
            return True
        return False

    def set_personal(self, personal: Personal) -> None:
        self.personal = personal
