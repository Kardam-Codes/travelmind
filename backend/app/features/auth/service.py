import hashlib
import os
from fastapi import HTTPException
from sqlmodel import Session

from app.core.security import create_access_token
from app.database.models.user import User
from app.features.orgs.service import create_org_with_owner, list_user_orgs, get_org
from app.repositories.user_repository import create_user, get_user_by_email
from app.schemas.org import OrganizationRead
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


def sign_up_user(session: Session, payload: SignUpRequest) -> tuple[User, str, list[OrganizationRead], int | None]:
    existing_user = get_user_by_email(session, payload.email.strip().lower())
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists.")

    user = User(
        name=payload.name,
        email=payload.email.strip().lower(),
        password_hash=_hash_password(payload.password),
        auth_provider="local",
    )
    user = create_user(session, user)
    org_name = f"{user.name or user.email.split('@')[0]}'s Workspace"
    org = create_org_with_owner(session, org_name, user.id)
    token = create_access_token(user.id)
    orgs = _build_user_orgs(session, user.id)
    return user, token, orgs, org.id


def login_user(session: Session, payload: LoginRequest) -> tuple[User, str, list[OrganizationRead], int | None]:
    user = get_user_by_email(session, payload.email.strip().lower())
    if not user or not _verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid email or password.")

    token = create_access_token(user.id)
    orgs = _build_user_orgs(session, user.id)
    if not orgs:
        org_name = f"{user.name or user.email.split('@')[0]}'s Workspace"
        org = create_org_with_owner(session, org_name, user.id)
        orgs = _build_user_orgs(session, user.id)
        default_org_id = org.id
    else:
        default_org_id = orgs[0].id
    return user, token, orgs, default_org_id


def google_auth_user(session: Session, payload: GoogleAuthRequest) -> tuple[User, str, list[OrganizationRead], int | None]:
    email = payload.email.strip().lower()
    user = get_user_by_email(session, email)
    if user:
        token = create_access_token(user.id)
        orgs = _build_user_orgs(session, user.id)
        if not orgs:
            org_name = f"{user.name or user.email.split('@')[0]}'s Workspace"
            org = create_org_with_owner(session, org_name, user.id)
            orgs = _build_user_orgs(session, user.id)
            default_org_id = org.id
        else:
            default_org_id = orgs[0].id
        return user, token, orgs, default_org_id

    user = User(
        name=payload.name,
        email=email,
        password_hash=_hash_password("google-auth-placeholder"),
        auth_provider="google",
    )
    user = create_user(session, user)
    org_name = f"{user.name or user.email.split('@')[0]}'s Workspace"
    org = create_org_with_owner(session, org_name, user.id)
    token = create_access_token(user.id)
    orgs = _build_user_orgs(session, user.id)
    return user, token, orgs, org.id


def _build_user_orgs(session: Session, user_id: int) -> list[OrganizationRead]:
    memberships = list_user_orgs(session, user_id)
    orgs = []
    for membership in memberships:
        org = get_org(session, membership.organization_id)
        orgs.append(OrganizationRead(id=org.id, name=org.name, slug=org.slug))
    return orgs
