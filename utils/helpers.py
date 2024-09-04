from utils.models import Event
from fastapi import HTTPException
from datetime import datetime


def get_start_of_today() -> datetime:
    """returns today, but with H:M:S set to 00:00:00"""
    now = datetime.now()
    now = now.replace(hour=0, minute=0, second=0, microsecond=0)

    return now


def assert_event_has_unique_id(event_id: int, all_events: list[Event]):
    """checks if event_id is unique vs all_events"""
    ids = [x.id for x in all_events]

    if event_id in ids:
        raise HTTPException(
            status_code=400,
            detail=f"id={event_id} has already been taken, please use a different id",
        )


def find_event_from_id(event_id: int, all_events: list[Event]) -> Event:
    """returns matching event if found"""

    try:
        match = next(x for x in all_events if x.id == event_id)
    except StopIteration:
        raise HTTPException(
            status_code=404, detail=f"events with id {event_id} not found"
        )

    return match


def find_events_from_time(time: datetime, all_events: list[Event]) -> list[Event]:
    """returns list of matching events. Can be multiple as events can have the same time"""

    matches = [x for x in all_events if x.time == time]

    if not matches:
        raise HTTPException(
            status_code=404, detail=f"events with time {time} not found"
        )

    return matches


def find_events_between_times(
    from_time: None | datetime, to_time: datetime, all_events: list[Event]
) -> list[Event]:
    """returns list of matching events. Can be multiple as events can have the same time"""

    if not from_time:
        from_time = get_start_of_today()

    matches = [x for x in all_events if x.time > from_time and x.time < to_time]

    if not matches:
        raise HTTPException(
            status_code=404,
            detail=f"no events found between times {from_time} and {to_time}",
        )

    return matches
