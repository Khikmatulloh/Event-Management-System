from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.dependencies import get_db
from app.models.models import Event, EventRegistration, User
from app.schemas.schemas import EventCreate, EventUpdate, EventResponse, RegistrationResponse
from app.routers.auth import get_current_user
from typing import List

router = APIRouter(prefix="/events", tags=["Events"])


@router.get("/", response_model=List[EventResponse])
def get_events(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(Event).filter(Event.is_active == True).offset(skip).limit(limit).all()


@router.get("/{id}", response_model=EventResponse)
def get_event(id: int, db: Session = Depends(get_db)):
    event = db.query(Event).filter(Event.id == id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return event


@router.post("/", response_model=EventResponse)
def create_event(event: EventCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    new_event = Event(**event.dict(), organizer_id=current_user.id)
    db.add(new_event)
    db.commit()
    db.refresh(new_event)
    return new_event


@router.put("/{id}", response_model=EventResponse)
def update_event(id: int, event_update: EventUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    event = db.query(Event).filter(Event.id == id).first()
    if not event or event.organizer_id != current_user.id:
        raise HTTPException(status_code=403, detail="Unauthorized")
    for key, value in event_update.dict().items():
        setattr(event, key, value)
    db.commit()
    db.refresh(event)
    return event


@router.delete("/{id}")
def delete_event(id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    event = db.query(Event).filter(Event.id == id).first()
    if not event or event.organizer_id != current_user.id:
        raise HTTPException(status_code=403, detail="Unauthorized")
    db.delete(event)
    db.commit()
    return {"msg": "Event deleted"}


@router.post("/{id}/register", response_model=RegistrationResponse)
def register_event(id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    event = db.query(Event).filter(Event.id == id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    if len(event.registrations) >= event.max_participants:
        raise HTTPException(status_code=400, detail="Max participants reached")
    already = db.query(EventRegistration).filter_by(event_id=id, user_id=current_user.id).first()
    if already:
        raise HTTPException(status_code=400, detail="Already registered")
    reg = EventRegistration(event_id=id, user_id=current_user.id)
    db.add(reg)
    db.commit()
    db.refresh(reg)
    return reg

@router.delete("/{id}/register")
def cancel_registration(id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    reg = db.query(EventRegistration).filter_by(event_id=id, user_id=current_user.id).first()
    if not reg:
        raise HTTPException(status_code=404, detail="Not registered")
    db.delete(reg)
    db.commit()
    return {"msg": "Registration cancelled"}

@router.get("/{id}/participants")
def participants(id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    registrations = db.query(EventRegistration).filter_by(event_id=id).all()
    return [{"user_id": r.user_id} for r in registrations]
