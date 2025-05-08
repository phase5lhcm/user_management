from pydantic import BaseModel
from datetime import datetime

class EventBase(BaseModel):
    """Base schema for Event model."""
    title: str
    description: str
    start_time: datetime
    end_time: datetime


class EventCreate(EventBase):
    """Schema for creating a new event."""
    pass

class EventUpdate(EventBase):
    """Schema for updating an existing event."""
    pass

#To structure and serialize outgoing event data, we define the EventOut schema.
class EventOut(EventBase):
    """Schema for returning event data to the client (e.g., GET or POST response)"""
    id: int
    creator_id: int

    class Config:
        orm_mode = True
        from_attributes = True


