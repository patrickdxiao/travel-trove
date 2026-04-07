from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import engine, Base, get_db
from crud import get_or_fetch_activities
import models

Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/activities")
async def get_activities(city: str, country: str, db: Session = Depends(get_db)):
    if not city or not country:
        raise HTTPException(status_code=400, detail="city and country are required")

    activities = await get_or_fetch_activities(db, city, country)

    return [
        {
            "id": str(a.id),
            "name": a.name,
            "photo_urls": a.photo_urls,
            "website_url": a.website_url,
            "category": a.category,
            "city": a.city,
            "country": a.country,
            "rating": a.rating,
        }
        for a in activities
    ]
