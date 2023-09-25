from pydantic import BaseModel
from typing import List, Dict
from datetime import date


class UserRegistration(BaseModel):
    name: str
    email: str
    password: str


class UserLogin(BaseModel):
    email: str
    password: str


class EventBase(BaseModel):
    name: str
    date: date
    location: str
    description: str
    invitees: List[str] = []
    rsvps: Dict[str, str] = {}


class EventCreate(EventBase):
    pass


class Event(EventBase):
    id: str

    class Config:
        orm_mode = True


class RSVPData(BaseModel):
    rsvp_status: str