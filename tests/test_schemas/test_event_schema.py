import pytest
from datetime import datetime, timedelta
from uuid import UUID, uuid4
from app.schemas.event import (
    EventBase,
    EventCreate,
    EventUpdate)

def test_event_create_valid():
    event = EventCreate(
        title="IS601 Web Development with Python",
        description="A comprehensive course on web development using Python.",
        start_time=datetime.now(),
        end_time=datetime.now() + timedelta(days=30),
        creator_id=uuid4(),
    )
    assert event.title == "IS601 Web Development with Python"
    assert event.description == "A comprehensive course on web development using Python."
    assert isinstance(event.start_time, datetime)