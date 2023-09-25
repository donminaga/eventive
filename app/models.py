from pydantic import BaseModel
from datetime import datetime
from typing import List, Dict


class UserRegistration(BaseModel):
    email: str
    password: str


class UserLogin(BaseModel):
    email: str
    password: str


class EventBase(BaseModel):
    name: str
    date: datetime
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
