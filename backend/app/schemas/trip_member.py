from sqlmodel import SQLModel


class TripMemberCreate(SQLModel):
    user_id: int
    role: str


class TripMemberUpdate(SQLModel):
    role: str


class TripMemberRead(SQLModel):
    id: int
    trip_id: int
    user_id: int
    role: str
