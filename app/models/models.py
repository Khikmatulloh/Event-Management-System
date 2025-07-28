from datetime import UTC, datetime
from sqlalchemy import ForeignKey,Integer,String,Boolean,DateTime,Enum  
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
import enum


class RegistrationStatus(enum.Enum):
    confirmed = "confirmed"
    cancelled = "cancelled"
    waitlist = "waitlist"

class User(Base):
    __tablename__="users"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    username: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    events: Mapped[list["Event"]] = relationship(back_populates="organizer")

    registrations: Mapped[list["EventRegistration"]] = relationship(back_populates="user")
class Event(Base):
    __tablename__ = "events"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(String)
    date: Mapped[datetime] = mapped_column(DateTime)
    location: Mapped[str] = mapped_column(String)
    max_participants: Mapped[int] = mapped_column(Integer)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    organizer_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    organizer: Mapped["User"] = relationship(back_populates="events")
    registrations: Mapped[list["EventRegistration"]] = relationship(back_populates="event")


class EventRegistration(Base):
    __tablename__ = "registrations"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    event_id: Mapped[int] = mapped_column(ForeignKey("events.id"))

    user: Mapped["User"] = relationship(back_populates="registrations")
    event: Mapped["Event"] = relationship(back_populates="registrations")