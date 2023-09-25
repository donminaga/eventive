from fastapi import APIRouter, HTTPException, Header
from app.models import EventCreate, Event
from firebase_admin import firestore
from typing import List

db = firestore.client()
events_ref = db.collection('events')

router = APIRouter()


@router.post("/events/", response_model=Event)
def create_event(event: EventCreate, token: str = Header(None), email: str = Header(None)):
    if not token or not email:
        raise HTTPException(status_code=401, detail="Invalid token or email header")
    _, new_event = events_ref.add({
        "name": event.name,
        "date": event.date,
        "location": event.location,
        "description": event.description,
        "user_email": email,  # associate the event with a user
        "invitees": [],  # initialize invitees list
        "rsvps": {}  # initialize rsvps dictionary
    })
    return Event(id=new_event.id, **event.dict())


@router.get("/events/", response_model=list[Event])
def list_events(token: str = Header(None), email: str = Header(None)):
    if not token or not email:
        raise HTTPException(status_code=401, detail="Invalid token or email header")
    user_events = events_ref.where("user_email", "==", email).stream()
    return [Event(id=doc.id, **doc.to_dict()) for doc in user_events]


@router.post("/events/{event_id}/invite/")
def invite_to_event(event_id: str, invitees: List[str], token: str = Header(None), email: str = Header(None)):
    try:
        if not token or not email:
            raise HTTPException(status_code=401, detail="Invalid token or email header")

        event_ref = events_ref.document(event_id)
        event = event_ref.get()

        if not event.exists:
            raise HTTPException(status_code=404, detail="Event not found")

        if event.to_dict().get("user_email") != email:
            raise HTTPException(status_code=403, detail="Not authorized to send invites for this event")

        current_invitees = event.to_dict().get("invitees", [])

        updated_invitees = list(set(current_invitees + invitees))
        event_ref.update({"invitees": updated_invitees})

        return {"message": "Invites sent successfully"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/events/{event_id}/rsvp/")
def rsvp_to_event(event_id: str, rsvp_status: str, token: str = Header(None), email: str = Header(None)):
    if not token or not email:
        raise HTTPException(status_code=401, detail="Invalid token or email header")

    event_ref = events_ref.document(event_id)
    event = event_ref.get()

    if not event.exists:
        raise HTTPException(status_code=404, detail="Event not found")

    # Only invited users can RSVP
    if email not in event.get("invitees"):
        raise HTTPException(status_code=403, detail="Not invited to this event")

    # Update the RSVP status
    event_ref.update({"rsvps": {email: rsvp_status}})

    return {"message": f"RSVP as {rsvp_status} received"}
