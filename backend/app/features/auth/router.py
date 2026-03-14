from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.database.session import get_session
from app.features.auth.service import google_auth_user, login_user, sign_up_user
from app.schemas.auth import AuthResponse, GoogleAuthRequest, LoginRequest, SignUpRequest


router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/signup", response_model=AuthResponse)
def signup_endpoint(payload: SignUpRequest, session: Session = Depends(get_session)):
    user = sign_up_user(session, payload)
    return AuthResponse(message="Signup successful.", user_id=user.id, email=user.email)


@router.post("/login", response_model=AuthResponse)
def login_endpoint(payload: LoginRequest, session: Session = Depends(get_session)):
    user = login_user(session, payload)
    return AuthResponse(message="Login successful.", user_id=user.id, email=user.email)


@router.post("/google", response_model=AuthResponse)
def google_auth_endpoint(payload: GoogleAuthRequest, session: Session = Depends(get_session)):
    user = google_auth_user(session, payload)
    return AuthResponse(message="Google auth successful.", user_id=user.id, email=user.email)
