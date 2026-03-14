from datetime import datetime, timedelta, timezone
from typing import Optional

import jwt
from fastapi import Depends, Header, HTTPException, status
from sqlmodel import Session

from app.core.config import settings
from app.database.session import get_session
from app.database.models.user import User
from app.repositories.user_repository import get_user_by_id


def create_access_token(user_id: int) -> str:
    payload = {
        "sub": str(user_id),
        "exp": datetime.now(timezone.utc) + timedelta(minutes=settings.jwt_exp_minutes),
    }
    return jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)


def decode_access_token(token: str) -> int:
    try:
        payload = jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])
    except jwt.PyJWTError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token.") from exc

    subject = payload.get("sub")
    if not subject or not str(subject).isdigit():
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token subject.")

    return int(subject)


def get_current_user_id(authorization: Optional[str] = Header(None)) -> int:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing authentication token.")
    token = authorization.split(" ", 1)[1].strip()
    return decode_access_token(token)


def get_current_user(
    authorization: Optional[str] = Header(None),
    session: Session = Depends(get_session),
) -> User:
    user_id = get_current_user_id(authorization)
    user = get_user_by_id(session, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found.")
    return user


def get_current_org_id(x_org_id: Optional[str] = Header(None)) -> int:
    if not x_org_id or not str(x_org_id).isdigit():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="X-Org-Id header is required.")
    return int(x_org_id)
