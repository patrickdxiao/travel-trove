from sqlalchemy import Column, String, Float, DateTime, ARRAY, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import UUID
from database import Base
import uuid
import enum


class SwipeDirection(enum.Enum):
    left = "left"
    right = "right"


class Activity(Base):
    __tablename__ = "activities"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    photo_urls = Column(ARRAY(String), default=[])
    website_url = Column(String)
    category = Column(String)
    city = Column(String, nullable=False)
    country = Column(String, nullable=False)
    rating = Column(Float)
    fetched_at = Column(DateTime, nullable=False)


class Swipe(Base):
    __tablename__ = "swipes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id = Column(String, nullable=False)
    activity_id = Column(UUID(as_uuid=True), ForeignKey("activities.id"), nullable=False)
    direction = Column(Enum(SwipeDirection), nullable=False)
    swiped_at = Column(DateTime, nullable=False)
