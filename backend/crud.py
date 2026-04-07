from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from models import Activity
from places import fetch_activities_for_city

TTL_DAYS = 30


def is_city_data_fresh(db: Session, city: str) -> bool:
    cutoff = datetime.utcnow() - timedelta(days=TTL_DAYS)
    return db.query(Activity).filter(
        Activity.city == city,
        Activity.fetched_at >= cutoff
    ).first() is not None


async def get_or_fetch_activities(db: Session, city: str, country: str) -> list[Activity]:
    if is_city_data_fresh(db, city):
        return db.query(Activity).filter(Activity.city == city).all()

    db.query(Activity).filter(Activity.city == city).delete()
    db.commit()

    raw_activities = await fetch_activities_for_city(city, country)

    for data in raw_activities:
        activity = Activity(**data)
        db.add(activity)

    db.commit()

    return db.query(Activity).filter(Activity.city == city).all()
