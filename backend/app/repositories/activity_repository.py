from typing import List, Optional
from sqlmodel import Session, select
from app.database.models.activity import Activity


def get_activity_by_id(session: Session, activity_id: int) -> Optional[Activity]:
    statement = select(Activity).where(Activity.id == activity_id)
    return session.exec(statement).first()


def get_activities_by_city(session: Session, city_name: str) -> List[Activity]:
    statement = select(Activity).where(Activity.city == city_name).order_by(Activity.rating.desc())
    return list(session.exec(statement).all())


def get_activities_by_place(session: Session, place_id: int) -> List[Activity]:
    statement = select(Activity).where(Activity.linked_place_id == place_id)
    return list(session.exec(statement).all())


def get_activities_by_filters(
    session: Session,
    city_name: str,
    category: Optional[str] = None,
) -> List[Activity]:
    statement = select(Activity).where(Activity.city == city_name)

    if category:
        statement = statement.where(Activity.category == category)

    statement = statement.order_by(Activity.popularity_score.desc())
    return list(session.exec(statement).all())


def create_activity(session: Session, activity_data: Activity) -> Activity:
    session.add(activity_data)
    session.commit()
    session.refresh(activity_data)
    return activity_data
