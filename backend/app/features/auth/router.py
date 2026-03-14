from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.database.session import get_session
from app.features.auth.service import google_auth_user, login_user, sign_up_user
from app.schemas.auth import AuthResponse, GoogleAuthRequest, LoginRequest, SignUpRequest, MeResponse, UserRead
from app.core.security import get_current_user
from app.features.orgs.service import list_user_orgs, get_org
from app.schemas.org import OrganizationRead


router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/signup", response_model=AuthResponse)
def signup_endpoint(payload: SignUpRequest, session: Session = Depends(get_session)):
    user, token, orgs, default_org_id = sign_up_user(session, payload)
    return AuthResponse(
        message="Signup successful.",
        user_id=user.id,
        email=user.email,
        access_token=token,
        organizations=orgs,
        default_org_id=default_org_id,
    )


@router.post("/login", response_model=AuthResponse)
def login_endpoint(payload: LoginRequest, session: Session = Depends(get_session)):
    user, token, orgs, default_org_id = login_user(session, payload)
    return AuthResponse(
        message="Login successful.",
        user_id=user.id,
        email=user.email,
        access_token=token,
        organizations=orgs,
        default_org_id=default_org_id,
    )


@router.post("/google", response_model=AuthResponse)
def google_auth_endpoint(payload: GoogleAuthRequest, session: Session = Depends(get_session)):
    user, token, orgs, default_org_id = google_auth_user(session, payload)
    return AuthResponse(
        message="Google auth successful.",
        user_id=user.id,
        email=user.email,
        access_token=token,
        organizations=orgs,
        default_org_id=default_org_id,
    )


@router.get("/me", response_model=MeResponse)
def me_endpoint(
    session: Session = Depends(get_session),
    current_user=Depends(get_current_user),
):
    memberships = list_user_orgs(session, current_user.id)
    orgs = []
    for membership in memberships:
        org = get_org(session, membership.organization_id)
        orgs.append(OrganizationRead(id=org.id, name=org.name, slug=org.slug))
    default_org_id = orgs[0].id if orgs else None
    return MeResponse(
        user=UserRead(id=current_user.id, name=current_user.name, email=current_user.email),
        organizations=orgs,
        active_org_id=default_org_id,
    )
