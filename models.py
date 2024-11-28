from sqlalchemy import Boolean, Column, Integer, String, DateTime, UniqueConstraint
from database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

class Train(Base):
    __tablename__ = "trains"

    id = Column(Integer, primary_key=True, index=True)
    train_number = Column(String, unique=True, index=True)
    total_seats = Column(Integer)
    departure_station = Column(String)
    arrival_station = Column(String)
    departure_time = Column(DateTime)
    arrival_time = Column(DateTime)

class Passenger(Base):
    __tablename__ = "passengers"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    passport_number = Column(String, unique=True, index=True)
    train_number = Column(String, index=True)
    departure_station = Column(String)
    arrival_station = Column(String)
    departure_time = Column(DateTime)
    arrival_time = Column(DateTime)
    seat_number = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Добавляем ограничение на уникальность комбинации номера поезда и места
    __table_args__ = (
        UniqueConstraint('train_number', 'seat_number', name='unique_seat'),
    )
