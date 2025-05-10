import pytest
from datetime import datetime, timedelta
from uuid import UUID, uuid4
from app.schemas.event import (
    EventBase,
    EventCreate,
    EventUpdate)
from pydantic import ValidationError

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

def test_event_create_missing_title():
    with pytest.raises(ValidationError) as exc_info:
        EventCreate(
            description="No title here",
            start_date=datetime.now(),
            end_date=datetime.now() + timedelta(days=1),
            creator_id=uuid4()
        )

    errors = exc_info.value.errors()
    assert any(error["loc"] == ("title",) for error in errors)
    assert any(error["type"] == "missing" for error in errors)
