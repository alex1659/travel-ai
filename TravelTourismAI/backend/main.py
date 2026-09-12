from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy.orm import Session

from database import engine, Base, get_db

from models import (
    User,
    Destination,
    Trip,
    Feedback
)

from schemas import (
    UserCreate,
    UserLogin,
    DestinationCreate,
    TripCreate,
    ItineraryRequest,
    FeedbackCreate
)

from auth import (
    hash_password,
    verify_password,
    create_access_token
)

from recommendation import (
    generate_recommendations
)


# ==================================
# CREATE APP
# ==================================

app = FastAPI(
    title="AI Travel & Tourism Platform",
    description="AI-powered personalized travel platform",
    version="1.0"
)


# ==================================
# CORS
# ==================================

app.add_middleware(
    CORSMiddleware,

    allow_origins=["*"],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"]
)


# ==================================
# CREATE DATABASE TABLES
# ==================================

Base.metadata.create_all(
    bind=engine
)


# ==================================
# HOME
# ==================================

@app.get("/")
def home():

    return {
        "message": "AI Travel & Tourism Platform is running"
    }


# ==================================
# REGISTER
# ==================================

@app.post("/register")
def register(
    user: UserCreate,
    db: Session = Depends(get_db)
):

    existing_user = db.query(
        User
    ).filter(
        User.email == user.email
    ).first()


    if existing_user:

        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )


    new_user = User(

        name=user.name,

        email=user.email,

        password=hash_password(
            user.password
        )
    )


    db.add(new_user)

    db.commit()

    db.refresh(new_user)


    return {

        "message": "Registration successful",

        "user_id": new_user.id
    }


# ==================================
# LOGIN
# ==================================

@app.post("/login")
def login(
    user: UserLogin,
    db: Session = Depends(get_db)
):

    existing_user = db.query(
        User
    ).filter(
        User.email == user.email
    ).first()


    if not existing_user:

        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )


    if not verify_password(
        user.password,
        existing_user.password
    ):

        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )


    token = create_access_token(
        existing_user.id
    )


    return {

        "message": "Login successful",

        "access_token": token,

        "user": {

            "id": existing_user.id,

            "name": existing_user.name,

            "email": existing_user.email
        }
    }


# ==================================
# DESTINATIONS
# ==================================

@app.post("/destinations")
def create_destination(
    destination: DestinationCreate,
    db: Session = Depends(get_db)
):

    new_destination = Destination(

        name=destination.name,

        state=destination.state,

        country=destination.country,

        description=destination.description,

        latitude=destination.latitude,

        longitude=destination.longitude,

        budget=destination.budget,

        rating=destination.rating
    )


    db.add(new_destination)

    db.commit()

    db.refresh(new_destination)


    return new_destination


@app.get("/destinations")
def get_destinations(
    db: Session = Depends(get_db)
):

    return db.query(
        Destination
    ).all()


# ==================================
# CREATE TRIP
# ==================================

@app.post("/trips")
def create_trip(
    trip: TripCreate,
    db: Session = Depends(get_db)
):

    new_trip = Trip(

        user_id=1,

        destination_id=trip.destination_id,

        start_date=trip.start_date,

        end_date=trip.end_date,

        budget=trip.budget
    )


    db.add(new_trip)

    db.commit()

    db.refresh(new_trip)


    return {

        "message": "Trip created",

        "trip_id": new_trip.id
    }


# ==================================
# AI ITINERARY
# ==================================

@app.post("/generate-itinerary")
def generate_itinerary(
    request: ItineraryRequest
):

    itinerary = generate_recommendations(

        destination=request.destination,

        interests=request.interests,

        days=request.days
    )


    return {

        "destination": request.destination,

        "budget": request.budget,

        "days": request.days,

        "interests": request.interests,

        "itinerary": itinerary
    }


# ==================================
# FEEDBACK
# ==================================

@app.post("/feedback")
def create_feedback(
    feedback: FeedbackCreate,
    db: Session = Depends(get_db)
):

    new_feedback = Feedback(

        user_id=1,

        destination_id=feedback.destination_id,

        rating=feedback.rating,

        comment=feedback.comment
    )


    db.add(new_feedback)

    db.commit()

    db.refresh(new_feedback)


    return {

        "message": "Feedback submitted",

        "feedback_id": new_feedback.id
    }