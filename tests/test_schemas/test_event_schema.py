import pytest
from datetime import datetime, timedelta
from uuid import UUID, uuid4
from app.schemas.event import (
    EventBase,
    EventCreate,
    EventUpdate,
    EventOut)
from pydantic import ValidationError
from uuid import uuid1

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
            start_time=datetime.now(),
            end_time=datetime.now() + timedelta(days=1),
            creator_id=uuid4()
        )

    errors = exc_info.value.errors()
    assert any(error["loc"] == ("title",) for error in errors)
    assert any(error["type"] == "missing" for error in errors)

def test_event_create_invalid_start_date_type():
    with pytest.raises(ValidationError):
        EventCreate(
            title="Invalid Date",
            description="Bad type",
            start_time="not-a-date",
            end_time=datetime.now(),
            creator_id=uuid4()
        )

def test_event_create_invalid_creator_id_format():
    with pytest.raises(ValidationError):
        EventCreate(
            title="Bad Creator ID",
            description="Invalid UUID",
            start_time=datetime.now(),
            end_time=datetime.now() + timedelta(days=1),
            creator_id="123-not-a-uuid"
        )

def test_event_create_start_after_end():
    start = datetime.now()
    end = start - timedelta(days=1)  # Invalid

    event = EventCreate(
        title="Backwards Event",
        description="Ends before it starts",
        start_time=start,
        end_time=end,
        creator_id=uuid4()
    )

    assert event.start_time > event.end_time

def test_event_out_schema_valid():
    out = EventOut(
        id=1,
        title="Webinar",
        description="Intro to FastAPI",
        start_time=datetime.now(),
        end_time=datetime.now() + timedelta(days=1),
        creator_id=uuid4(),
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    assert isinstance(out.id, int)
    assert isinstance(out.creator_id, UUID)

def test_event_create_no_description():
    event = EventCreate(
        title="Simple Event",
        start_time=datetime.now(),
        end_time=datetime.now() + timedelta(days=1),
        creator_id=uuid4()
    )
    assert event.description is None
