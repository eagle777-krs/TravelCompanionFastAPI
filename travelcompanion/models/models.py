from datetime import datetime
from typing import Optional
from sqlalchemy import String, Integer, ForeignKey, Float, DateTime, Boolean, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    telegram_id: Mapped[int] = mapped_column(Integer, unique=True, index=True)
    name: Mapped[str] = mapped_column(String(100))
    latitude: Mapped[float] = mapped_column(Float, index=True)
    longitude: Mapped[float] = mapped_column(Float, index=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    preferences: Mapped[list["UserPreference"]] = relationship(back_populates="user")
    history: Mapped[list["UserHistory"]] = relationship(back_populates="user")
    flights: Mapped[list["Flight"]] = relationship(back_populates="user")


class UserPreference(Base):
    __tablename__ = "user_preferences"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id", ondelete="CASCADE"), index=True)
    weight: Mapped[float] = mapped_column(Float)
    last_updated: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, index=True)

    user: Mapped["User"] = relationship(back_populates="preferences")
    category: Mapped["Category"] = relationship(back_populates="preferences")


class Place(Base):
    __tablename__ = "places"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id", ondelete="CASCADE"), index=True)
    name: Mapped[str] = mapped_column(String(200), index=True)
    rating: Mapped[Optional[float]] = mapped_column(Float, index=True)
    price_range: Mapped[Optional[str]] = mapped_column(String(50))
    latitude: Mapped[float] = mapped_column(Float, index=True)
    longitude: Mapped[float] = mapped_column(Float, index=True)
    api_source: Mapped[Optional[str]] = mapped_column(String(100))
    last_updated: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, index=True)

    history: Mapped[list["UserHistory"]] = relationship(back_populates="place")
    category: Mapped["Category"] = relationship(back_populates="place")


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, index=True)

    preferences: Mapped[list["UserPreference"]] = relationship(back_populates="category")
    place: Mapped[list["Place"]] = relationship(back_populates="category")
    history: Mapped[list["UserHistory"]] = relationship(back_populates="category")


class UserHistory(Base):
    __tablename__ = "users_history"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    place_id: Mapped[int] = mapped_column(ForeignKey("places.id", ondelete="CASCADE"), index=True)
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id", ondelete="CASCADE"), index=True)
    request_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, index=True)
    rating: Mapped[Optional[float]] = mapped_column(Float)

    user: Mapped["User"] = relationship(back_populates="history")
    place: Mapped["Place"] = relationship(back_populates="history")
    category: Mapped["Category"] = relationship(back_populates="history")


class Airport(Base):
    __tablename__ = "airports"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    iata_code: Mapped[str] = mapped_column(String(10), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(200))
    latitude: Mapped[float] = mapped_column(Float, index=True)
    longitude: Mapped[float] = mapped_column(Float, index=True)
    city: Mapped[str] = mapped_column(String(100), index=True)
    country: Mapped[str] = mapped_column(String(100), index=True)
    timezone: Mapped[Optional[str]] = mapped_column(String(50))

    dep_flights: Mapped[list["Flight"]] = relationship(
        foreign_keys="[Flight.dep_airport_id]", back_populates="dep_airport"
    )
    arr_flights: Mapped[list["Flight"]] = relationship(
        foreign_keys="[Flight.arr_airport_id]", back_populates="arr_airport"
    )


class Flight(Base):
    __tablename__ = "flights"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    flight_number: Mapped[str] = mapped_column(String(20), index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    dep_airport_id: Mapped[int] = mapped_column(ForeignKey("airports.id"), index=True)
    arr_airport_id: Mapped[int] = mapped_column(ForeignKey("airports.id"), index=True)
    dep_time: Mapped[datetime] = mapped_column(DateTime, index=True)
    arr_time: Mapped[datetime] = mapped_column(DateTime, index=True)

    user: Mapped["User"] = relationship(back_populates="flights")
    dep_airport: Mapped["Airport"] = relationship(
        foreign_keys=[dep_airport_id], back_populates="dep_flights"
    )
    arr_airport: Mapped["Airport"] = relationship(
        foreign_keys=[arr_airport_id], back_populates="arr_flights"
    )