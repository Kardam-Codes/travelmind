from typing import Optional
from sqlmodel import SQLModel


class MessageResponse(SQLModel):
    message: str


class ErrorResponse(SQLModel):
    detail: str


class HealthResponse(SQLModel):
    status: str = "ok"
    app_name: Optional[str] = None
