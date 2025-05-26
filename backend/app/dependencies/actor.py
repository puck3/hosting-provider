from typing import Annotated

from fastapi import Depends, HTTPException
from pydantic import BaseModel
from starlette.status import HTTP_401_UNAUTHORIZED

from app.core.security import JWT
from app.dependencies.jwt import get_access_token, get_jwt_access
from app.models.user import Role


class Actor(BaseModel):
    user_id: int
    role: Role


def get_actor(
    access_token: Annotated[str, Depends(get_access_token)],
    jwt_access: Annotated[JWT, Depends(get_jwt_access)],
) -> Actor:
    try:
        payload = jwt_access.validate_token(access_token)
        return Actor(user_id=payload["sub"], role=payload["role"])
    except Exception as e:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Invalid token.",
        ) from e
