from pydantic import BaseModel
from typing import List
from datetime import date


# -------------------------
# USER
# -------------------------

class UserCreate(BaseModel):
    name: str
    email: str
    password: str


class UserLogin(BaseModel):
    email: str
    password: str


# -------------------------
# DESTINATION
# -------------------------

class DestinationCreate(BaseModel):
    name: str
    state: str
    country: str
    description: str
    latitude: float
    longitude: float
    budget: float
    rating: float


# -------------------------
# TRIP
# -------------------------

class TripCreate(BaseModel):
    destination_id: int
    start_date: date
    end_date: date
    budget: float


# -------------------------
# ITINERARY
# -------------------------

class ItineraryRequest(BaseModel):
    destination: str
    days: int
    budget: float
    interests: List[str]


# -------------------------
# FEEDBACK
# -------------------------

class FeedbackCreate(BaseModel):
    destination_id: int
    rating: int
    comment: str