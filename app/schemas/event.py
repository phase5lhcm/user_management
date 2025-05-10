from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class EventBase(BaseModel):
    """Base schema for Event model."""
    title: str = Field(..., max_length=255, example="This is a title")
    description: Optional[str] = Field(None, max_length=1000, example="This is a description")
    start_time: datetime
    end_time: datetime


class EventCreate(EventBase):
    """Schema for creating a new event."""
    creator_id: int = Field(..., example=1)

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


