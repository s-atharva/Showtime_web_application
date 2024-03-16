from sqlalchemy.ext.declarative import DeferredReflection
from sqlalchemy.orm import declarative_base, relationship
import uuid
from datetime import datetime, date
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime, JSON, Date
from .db_engine import DBEngine

Base = declarative_base(cls=DeferredReflection)


class User(Base):
    __tablename__ = 'users'
    id = Column(String(50), default=str(uuid.uuid4()), primary_key=True)
    name = Column(String(50))
    is_admin = Column(Boolean)
    user_name = Column(String(50))
    password = Column(String(50))
    bookings = relationship("Booking", back_populates="user")


def generate_uuid():
    return str(uuid.uuid4())


class Venue(Base):
    __tablename__ = 'venues'

    id = Column(String(50), default=generate_uuid(), primary_key=True)
    name = Column(String(50))
    address = Column(String(50))
    capacity = Column(Integer)
    city_id = Column(String(50), ForeignKey('cities.id'))
    city = relationship("City", back_populates="venues")
    shows = relationship("Show", back_populates="venue")


class City(Base):
    __tablename__ = 'cities'
    id = Column(String(50), default=str(uuid.uuid4()), primary_key=True)
    name = Column(String(50), unique=True)
    is_active = Column(Integer, default=1)
    venues = relationship("Venue", back_populates="city")


class Movie(Base):
    __tablename__ = "movies"
    id = Column(String(50), default=str(uuid.uuid4()), primary_key=True)
    name = Column(String(50))
    tags = Column(JSON)
    release_date = Column(Date)
    last_updated = Column(DateTime, default=datetime.now())
    shows = relationship("Show", back_populates="movie")


class Show(Base):
    __tablename__ = 'shows'
    id = Column(String(50), default=str(uuid.uuid4()), primary_key=True)
    slot = Column(String(50))
    price = Column(Integer)
    last_updated = Column(DateTime, default=datetime.now())
    event_date = Column(Date)
    # this is how you can use it datetime.date(2023, 4, 22)
    booking_count = Column(Integer, default=0)
    movie_id = Column(String(50), ForeignKey("movies.id"))
    movie = relationship("Movie", back_populates="shows")
    venue_id = Column(String(50), ForeignKey("venues.id"))
    venue = relationship("Venue", back_populates="shows")
    bookings = relationship("Booking", back_populates="show")


class Booking(Base):
    __tablename__ = 'bookings'
    id = Column(String(50), default=str(uuid.uuid4()), primary_key=True)
    tickets_count = Column(Integer)
    show_id = Column(String(50), ForeignKey("shows.id"))
    user_id = Column(String(50), ForeignKey("users.id"))
    show = relationship("Show", back_populates="bookings")
    user = relationship("User", back_populates="bookings")
    booked_at = Column(DateTime, default=datetime.now())


def create_db_models():
    engine = DBEngine.get_db_engine()
    Base.metadata.create_all(engine, Base.metadata.tables.values(), checkfirst=True)
    Base.prepare(engine)


create_db_models()
