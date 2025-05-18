from datetime import timedelta, timezone, datetime
import jwt
from pydantic import BaseModel


class JWT(BaseModel):
    def __init__(
        self,
        token_type: str,
        secret_key: str,
        algorithm: str,
        expires_delta_minutes: int,
    ):
        self._token_type = token_type
        self._secret_key = secret_key
        self._algorithm = algorithm
        self._expires_delta_minutes = expires_delta_minutes

    def create_token(
        self,
        data: dict,
    ) -> str:
        expire = self._calculate_expire()
        to_encode = self._create_payload(data, expire)
        token = self._encode(to_encode)
        return token

    def _calculate_expire(self):
        delta = timedelta(minutes=self._expires_delta_minutes)
        now = datetime.now(timezone.utc)
        return now + delta

    def _create_payload(self, data: dict, expire: datetime) -> dict:
        payload = data.copy()
        payload.update({"exp": expire, "type": self._token_type})
        return payload

    def _encode(self, payload: dict) -> str:
        encoded_jwt = jwt.encode(
            payload, self._secret_key, algorithm=self._algorithm
        )
        return encoded_jwt

    def validate_token(self, token: str) -> dict:
        payload = self._decode(token)
        if payload.get("type") != self._token_type:
            raise jwt.InvalidTokenError("Invalid token type")

        return payload

    def _decode(self, token: str) -> dict:
        payload = jwt.decode(
            token, self._secret_key, algorithms=[self._algorithm]
        )
        return payload
