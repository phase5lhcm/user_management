from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
from dependencies import get_db, get_current_user
from models.event import Event
from schemas.event import EventCreate, EventUpdate, EventOut
from utils.auth import is_admin_or_manager
from utils.dependencies import get_db

router = APIRouter(prefix="/events", tags=["Events"])

#Create endpoint to create a new event
@router.post("/events", response_model=EventOut)
def create_event(event: EventCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    is_admin_or_manager(user)
    new_event = Event(**event.model_dump(), creator_id=user.id)
    db.add(new_event)
    db.commit()
    db.refresh(new_event)
    return new_event

#Browse endpoint to get/list all events
router.get("/events", response_model=list[EventOut])
async def list_events(
        db: AsyncSession = Depends(get_db),
        user=Depends(get_current_user) 
):
    is_admin_or_manager(user)
    result = await db.execute(select(Event))
    events = result.scalars().all()
    return events

#GET endpoint to get a specific event by ID
router.get("/{event_id}", response_model=EventOut)
async def get_event(
        event_id: int,
        db: AsyncSession = Depends(get_db),
        user: dict = Depends(get_current_user)
):
    is_admin_or_manager(user)
    result = await db.execute(select(Event).where(Event.id == event_id))
    event = result.scalars_one_or_none()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return event

#Update endpoint to update an existing event
@router.put("/{event_id}", response_model=EventOut)
async def update_event(
    event_id: int,
    updated_data: EventUpdate,
    db: AsyncSession = Depends(get_db),
    user: dict = Depends(get_current_user)
):
    is_admin_or_manager(user)
    result = await db.execute(select(Event).where(Event.id == event_id))
    event = result.scalars_one_or_none()

    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    
    #Now we update the event fields with the new data
    for key, value in updated_data.model_dump(exclude_unset=True).items():
        setattr(event, key, value)
    
    await db.commit()
    await db.refresh(event)
    return event

#Delete endpoint to delete an event
router.delete("/{event_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_event(
        event_id: int,
        db: AsyncSession = Depends(get_db),
        user: dict = Depends(get_current_user)
):
    is_admin_or_manager(user)
    result = await db.execute(select(Event).where(Event.id == event_id))
    event = result.scalars_one_or_none()

    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    
    await db.delete(event)
    await db.commit()
    return {"detail": "Event deleted successfully"}

