from fastapi import APIRouter, HTTPException, Header
from app.models import EventCreate, Event, RSVPData
from datetime import datetime
from firebase_admin import firestore
from typing import List

db = firestore.client()
events_ref = db.collection('events')

router = APIRouter()


@router.post("/events/", response_model=Event)
def create_event(event: EventCreate, token: str = Header(None), email: str = Header(None)):
    if not token or not email:
        raise HTTPException(status_code=401, detail="Invalid token or email header")

    # Convert date object to string
    event_date_str = event.date.strftime("%Y-%m-%d")

    _, new_event = events_ref.add({
        "name": event.name,
        "date": event_date_str,
        "location": event.location,
        "description": event.description,
        "user_email": email,  # associate the event with a user
        "invitees": event.invitees,  # initialize invitees list
        "rsvps": {}  # initialize rsvps dictionary
    })
    return Event(id=new_event.id, **event.dict())


@router.get("/events/", response_model=List[Event])
def list_events(token: str = Header(None), email: str = Header(None)):
    if not token or not email:
        raise HTTPException(status_code=401, detail="Invalid token or email header")

    # Fetch events where the user is the organizer
    user_events = events_ref.where("user_email", "==", email).stream()

    # Fetch events where the user is an invitee
    invited_events = events_ref.where("invitees", "array_contains", email).stream()

    event_list = []

    # Helper function to process events and append to event_list
    def process_events(event_stream):
        for doc in event_stream:
            event_data = doc.to_dict()
            # Convert the date string back to a date object
            event_data["date"] = datetime.strptime(event_data["date"], "%Y-%m-%d").date()
            # Include user_email in the event data
            event_data["user_email"] = doc.to_dict().get("user_email")
            event_list.append(Event(id=doc.id, **event_data))

    # Process the fetched events
    process_events(user_events)
    process_events(invited_events)

    # Remove duplicates based on event IDs
    unique_event_list = list({event.id: event for event in event_list}.values())

    return unique_event_list


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
        current_invitees = [inv for inv in current_invitees if inv.strip() != ""]
        updated_invitees = list(set(current_invitees + invitees))

        event_ref.update({"invitees": updated_invitees})

        return {"message": "Invites sent successfully"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/events/{event_id}/rsvp/")
def rsvp_to_event(event_id: str, rsvp_data: RSVPData, token: str = Header(None), email: str = Header(None)):
    rsvp_status = rsvp_data.rsvp_status
    if not token or not email:
        raise HTTPException(status_code=401, detail="Invalid token or email header")

    event_ref = events_ref.document(event_id)
    event = event_ref.get()

    if not event.exists:
        raise HTTPException(status_code=404, detail="Event not found")

    event_data = event.to_dict()

    # Check if the user is the event creator or if they are in the invitees list
    if email != event_data.get("user_email") and email not in event_data.get("invitees", []):
        raise HTTPException(status_code=403, detail="Not invited to this event")

    # Update the RSVP status
    event_ref.update({f"rsvps.{email}": rsvp_status})

    return {"message": f"RSVP as {rsvp_status} received"}


@router.delete("/events/{event_id}/")
def delete_event(event_id: str, token: str = Header(None), email: str = Header(None)):
    if not token or not email:
        raise HTTPException(status_code=401, detail="Invalid token or email header")

    event_ref = events_ref.document(event_id)
    event = event_ref.get()

    if not event.exists:
        raise HTTPException(status_code=404, detail="Event not found")

    if event.to_dict().get("user_email") != email:
        raise HTTPException(status_code=403, detail="Not authorized to delete this event")

    event_ref.delete()

    return {"message": "Event deleted successfully"}
