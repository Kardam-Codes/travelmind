from typing import List

from app.database.models.place import Place


def limit_places_by_duration(places: List[Place], duration_days: int) -> List[Place]:
    if duration_days <= 2:
        return places[:4]
    if duration_days <= 4:
        return places[:8]
    return places[:12]
