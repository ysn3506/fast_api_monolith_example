from datetime import UTC, datetime, timedelta
from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pwdlib import PasswordHash
from sqlmodel import Session

from .db_config import get_db_session, get_settings
from .models import auth

ACCESS_TOKEN_EXPIRE_DURATION = 60
JWT_ALGORITHM = "H256"

security_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

password_hash = PasswordHash.recommended()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_hash.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return password_hash.hash(password)


def create_access_token(*, subject: str, expires_delta: timedelta | None = None) -> str:
    expires_at = datetime(
        datetime.now(UTC) + (expires_delta or timedelta(ACCESS_TOKEN_EXPIRE_DURATION))
    )
    payload = {"sub": subject, "exp": expires_at}

    return jwt.encode(payload, get_settings().jwt_secret_key.get_secret_value(), JWT_ALGORITHM)


def get_current_user(
    token: Annotated(str, Depends(security_scheme)),
    session: Annotated(Session, Depends(get_db_session)),
) -> auth.User:
    settings = get_settings()
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Unauthorized access try",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, settings.jwt_secret_key.get_secret_value(), JWT_ALGORITHM)
        user_id_str: int | None = payload.get("sub")
        if user_id_str is None:
            raise (credentials_exception)

        user_id = int(user_id_str)
    except (jwt.InvalidTokenError, ValueError) as exc:
        raise (credentials_exception) from exc

    user = session.get(auth.User, user_id)
    if user is None or not user.is_active:
        raise credentials_exception

    return user
