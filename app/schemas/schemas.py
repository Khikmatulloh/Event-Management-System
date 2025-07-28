# app/schemas/schemas.py
from pydantic import BaseModel, EmailStr
from datetime import datetime
from enum import Enum
from typing import Optional

class RegistrationStatus(str, Enum):
    confirmed = "confirmed"
    cancelled = "cancelled"
    waitlist = "waitlist"

class UserBase(BaseModel):
    email: EmailStr
    username: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool
    is_verified: bool
    created_at: datetime

    class Config:
        orm_mode = True

class EventBase(BaseModel):
    title: str
    description: str
    date: datetime
    location: str
    max_participants: int

class EventCreate(EventBase):
    pass

class EventUpdate(EventBase):
    pass

class EventResponse(EventBase):
    id: int
    organizer_id: int
    is_active: bool

    class Config:
        orm_mode = True

class RegistrationResponse(BaseModel):
    id: int
    user_id: int
    event_id: int

    class Config:
        orm_mode = True