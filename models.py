from passlib.context import CryptContext
from sqlalchemy import Boolean, Column, Integer, SmallInteger, ForeignKey, String, DateTime, UniqueConstraint
from sqlalchemy.orm import relationship
from database import Base, SessionLocal
from datetime import datetime


class Passenger(Base):
    __tablename__ = "Passengers"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    first_name = Column(String, index=True, nullable=False)
    last_name = Column(String, index=True, nullable=False)
    middle_name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    series_passport = Column(SmallInteger, nullable=False)
    number_passport = Column(Integer, nullable=False)


class City(Base):
    __tablename__ = "City"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    name = Column(String)


class Station(Base):
    __tablename__ = "Stations"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    name_station = Column(String, nullable=False, unique=True)
    city_id = Column(Integer, ForeignKey(City.id), nullable=False)


class Train(Base):
    __tablename__ = "Trains"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    train_name = Column(String, unique=True)
    total_seats = Column(Integer)


class User(Base):
    __tablename__ = "Users"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    username = Column(String, nullable=False, index=True)
    firstname = Column(String, nullable=False, index=True)
    lastname = Column(String, nullable=False, index=True)
    middle_name = Column(String, index=True)
    password = Column(String, nullable=False, index=True)
    email = Column(String, nullable=False, index=True)
    is_admin = Column(Boolean, nullable=False)

    # Добавляем ограничение на уникальность комбинации номера поезда и места
    __table_args__ = (
        UniqueConstraint('username', name='unique_username'),
        UniqueConstraint('email', name='unique_mail'),
    )


class Ticket(Base):
    __tablename__ = "Tickets"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    train_id = Column(Integer, ForeignKey(Train.id))
    departure_station_id = Column(Integer, ForeignKey(Station.id))
    arrival_station_id = Column(Integer, ForeignKey(Station.id))
    passenger_id = Column(Integer, ForeignKey(Passenger.id))
    departure_time = Column(DateTime, nullable=False)
    arrival_time = Column(DateTime, nullable=False)
    seat_number = Column(Integer, nullable=False)
    cashier_id = Column(Integer, ForeignKey(User.id))

    train = relationship(Train)
    passenger = relationship(Passenger)
    cashier = relationship(User)

    departure_station = relationship(Station, foreign_keys=[departure_station_id])
    arrival_station = relationship(Station, foreign_keys=[arrival_station_id])


def add_default_data():
    with SessionLocal() as db:
        if not db.query(Train).first():
            db.add(Train(
                train_name="Ласточка",
                total_seats=443,
            ))
            db.commit()

        if not db.query(City).first():
            db.add(City(
                name="Петербург",
            ))
            db.commit()

        if not db.query(Station).first():
            city = db.query(City).first()
            db.add(Station(
                name_station="Москва",
                city_id=city.id,
            ))
            db.commit()

        if not db.query(User).first():
            db.add(User(
                username="admin",
                firstname="Administrator",
                lastname="Administrator",
                middle_name="Administrator",
                password=CryptContext(schemes=["bcrypt"], deprecated="auto").hash("admin"),
                email="admin@db.local",
                is_admin=True,
            ))
            db.commit()
