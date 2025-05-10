from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from typing import Optional
from uuid import UUID

class EventBase(BaseModel):
    """Base schema for Event model."""
    title: str = Field(..., max_length=255, example="This is a title")
    description: Optional[str] = Field(None, max_length=1000, example="This is a description")
    start_time: datetime
    end_time: datetime


class EventCreate(EventBase):
    """Schema for creating a new event."""
    creator_id: UUID = Field(..., example="d290f1ee-6c54-4b01-90e6-d701748f0851")

    @field_validator("creator_id")
    @classmethod
    def validate_creator_id(cls, value: UUID) -> UUID:
        if value.version != 4:
            raise ValueError("creator_id must be a valid UUID v4")
        return value

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


