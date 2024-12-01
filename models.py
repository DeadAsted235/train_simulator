from sqlalchemy import Boolean, Column, Integer, SmallInteger, ForeignKey, VARCHAR, String, DateTime, UniqueConstraint
from database import Base
from datetime import datetime


class Passenger(Base):
    __tablename__ = "Passengars"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    first_name = Column(String, index=True, nullable=False)
    last_name = Column(String, index=True, nullable=False)
    middle_name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    series_passport = Column(SmallInteger, nullable=False)
    number_passport = Column(Integer, nullable=False)


class Station(Base):
    __tablename__ = "Stations"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    name_station = Column(VARCHAR, nullable=False, index=True)
    city = Column(VARCHAR, index=True)


class Train(Base):
    __tablename__ = "Trains"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    train_name = Column(String, unique=True, index=True)
    total_seats = Column(Integer)
    departure_station = Column(Integer, ForeignKey(Station.id))
    arrival_station = Column(Integer, ForeignKey(Station.id))


class Ticket(Base):
    __tablename__ = "Tickets"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    train_id = Column(Integer, ForeignKey(Train.id))
    departure_station_id = Column(Integer, ForeignKey(Station.id))
    arrival_station_id = Column(Integer, ForeignKey(Station.id))
    passenger_id = Column(Integer, ForeignKey(Passenger.id))
    departure_time = Column(DateTime, nullable=False)
    arrival_time = Column(DateTime, nullable=False)
    first_name = Column(String, index=True, nullable=False)
    last_name = Column(String, index=True, nullable=False)
    middle_name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    series_passport = Column(SmallInteger, nullable=False)
    number_passport = Column(Integer, nullable=False)


class User(Base):
    __tablename__ = "Users"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    username = Column(String, nullable=False, index=True)
    firstname = Column(String, nullable=False, index=True)
    lastname = Column(String, nullable=False, index=True)
    middlename = Column(String, index=True)
    password = Column(String, nullable=False, index=True)
    email = Column(String, nullable=False, index=True)

    # Добавляем ограничение на уникальность комбинации номера поезда и места
    __table_args__ = (
        UniqueConstraint('username', name='unique_username'),
        UniqueConstraint('email', name='unique_mail'),
    )
