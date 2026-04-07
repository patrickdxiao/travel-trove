import os
import httpx
from datetime import datetime

GOOGLE_PLACES_API_KEY = os.getenv("GOOGLE_PLACES_API_KEY")
PLACES_URL = "https://places.googleapis.com/v1/places:searchText"

CATEGORIES = [
    "restaurant",
    "tourist attraction",
    "resort",
    "museum",
    "night market",
    "hiking trail",
    "beach",
    "shopping mall",
    "amusement park",
    "spa",
]


async def fetch_activities_for_city(city: str, country: str) -> list[dict]:
    activities = []

    async with httpx.AsyncClient() as client:
        for category in CATEGORIES:
            query = f"{category} in {city}, {country}"

            response = await client.post(
                PLACES_URL,
                headers={
                    "Content-Type": "application/json",
                    "X-Goog-Api-Key": GOOGLE_PLACES_API_KEY,
                    "X-Goog-FieldMask": "places.displayName,places.rating,places.websiteUri,places.photos,places.primaryTypeDisplayName",
                },
                json={"textQuery": query, "pageSize": 5},
            )

            if response.status_code != 200:
                continue

            places = response.json().get("places", [])

            for place in places:
                photo_urls = []
                for photo in place.get("photos", [])[:3]:
                    photo_name = photo.get("name")
                    if photo_name:
                        photo_urls.append(
                            f"https://places.googleapis.com/v1/{photo_name}/media?maxWidthPx=800&key={GOOGLE_PLACES_API_KEY}"
                        )

                activities.append({
                    "name": place.get("displayName", {}).get("text", ""),
                    "photo_urls": photo_urls,
                    "website_url": place.get("websiteUri"),
                    "category": place.get("primaryTypeDisplayName", {}).get("text", category),
                    "city": city,
                    "country": country,
                    "rating": place.get("rating"),
                    "fetched_at": datetime.utcnow(),
                })

    return activities
