from fastapi import FastAPI
from datetime import datetime
from utils.models import Event

from utils.helpers import (
    assert_event_has_unique_id,
    find_event_from_id,
    find_events_from_time,
    find_events_between_times,
)

ALL_EVENTS = []
app = FastAPI()


@app.get("/")
def root():
    return {"message": "Welcome To Amin's Calendar API :)"}


@app.post("/events")
def create_event(event: Event):
    """
    . creates and appends an event
    . event should follow schema defined by Event model
    . event should also follow iso-format date and have a unique id

    Errors
    . if date is invalid, pydantic error is raised
    . if id is not unique, HTTPException is raised
    """

    assert_event_has_unique_id(event_id=event.id, all_events=ALL_EVENTS)
    ALL_EVENTS.append(event)
    return ALL_EVENTS


@app.get("/events/{event_id}", response_model=Event)
def get_event_from_id(event_id: int) -> Event:
    """
    . returns event with given id. If not found, raises HTTPException
    """
    return find_event_from_id(event_id, ALL_EVENTS)


@app.get("/events", response_model=list[Event])
def get_events_from_time(
    datetime_format: datetime = None,
    from_time: datetime = None,
    to_time: datetime = None,
) -> list[Event]:
    """
    . if datetime_format provided, returns all events with that specific time
    . if only to_time provided, returns all events from today's date (with hour 0) to to_time
    . if both from_time and to_time provided, returns all events between the two dates
    . if no events are found, HTTPException is raised
    . if no query_parameters are provided, returns all events
    """

    if not datetime_format and not from_time and not to_time:
        return ALL_EVENTS

    if datetime_format:
        return find_events_from_time(datetime_format, ALL_EVENTS)

    return find_events_between_times(from_time, to_time, ALL_EVENTS)