from sqlalchemy import Column, Integer, String, Float, Text, Date
from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, nullable=False, index=True)
    password = Column(String(255), nullable=False)


class Destination(Base):
    __tablename__ = "destinations"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(150), nullable=False)
    state = Column(String(100))
    country = Column(String(100))

    description = Column(Text)

    latitude = Column(Float)
    longitude = Column(Float)

    budget = Column(Float)
    rating = Column(Float)


class Trip(Base):
    __tablename__ = "trips"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer)
    destination_id = Column(Integer)

    start_date = Column(Date)
    end_date = Column(Date)

    budget = Column(Float)


class Feedback(Base):
    __tablename__ = "feedback"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer)
    destination_id = Column(Integer)

    rating = Column(Integer)
    comment = Column(Text)