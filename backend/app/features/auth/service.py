import hashlib
import os
from fastapi import HTTPException
from sqlmodel import Session

from app.database.models.user import User
from app.repositories.user_repository import create_user, get_user_by_email
from app.schemas.auth import GoogleAuthRequest, LoginRequest, SignUpRequest


def _hash_password(password: str) -> str:
    salt = os.urandom(16)
    password_hash = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 100000)
    return f"{salt.hex()}:{password_hash.hex()}"


def _verify_password(password: str, stored_hash: str) -> bool:
    salt_hex, hash_hex = stored_hash.split(":")
    salt = bytes.fromhex(salt_hex)
    password_hash = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 100000)
    return password_hash.hex() == hash_hex


def sign_up_user(session: Session, payload: SignUpRequest) -> User:
    existing_user = get_user_by_email(session, payload.email.strip().lower())
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists.")

    user = User(
        name=payload.name,
        email=payload.email.strip().lower(),
        password_hash=_hash_password(payload.password),
        auth_provider="local",
    )
    return create_user(session, user)


def login_user(session: Session, payload: LoginRequest) -> User:
    user = get_user_by_email(session, payload.email.strip().lower())
    if not user or not _verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid email or password.")

    return user


def google_auth_user(session: Session, payload: GoogleAuthRequest) -> User:
    email = payload.email.strip().lower()
    user = get_user_by_email(session, email)
    if user:
        return user

    user = User(
        name=payload.name,
        email=email,
        password_hash=_hash_password("google-auth-placeholder"),
        auth_provider="google",
    )
    return create_user(session, user)
