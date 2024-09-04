import pytest
from datetime import datetime
from utils.models import Event
from utils.helpers import (
    find_event_from_id,
    find_events_from_time,
    find_events_between_times,
    get_start_of_today,
)
from tests.fixtures import MOCK_EVENTS

from fastapi import HTTPException


def test_get_start_of_today():
    expected_day = datetime.now().day
    expected_month = datetime.now().month
    expected_year = datetime.now().year
    expected_hour = 0
    expected_minute = 0
    expected_second = 0

    result = get_start_of_today()

    assert result.day == expected_day
    assert result.month == expected_month
    assert result.year == expected_year
    assert result.hour == expected_hour
    assert result.minute == expected_minute
    assert result.second == expected_second


def test_find_event_from_id_success():

    event = find_event_from_id(1, MOCK_EVENTS)
    assert event == MOCK_EVENTS[0]


def test_find_event_from_id_failure():

    event_id = 10
    with pytest.raises(HTTPException):
        find_event_from_id(event_id, MOCK_EVENTS)


def test_find_events_from_time_success():

    events = find_events_from_time(datetime(2024, 1, 1), MOCK_EVENTS)
    assert len(events) == 1
    event = events[0]
    assert event == MOCK_EVENTS[0]

    events = find_events_from_time(datetime(2024, 2, 1), MOCK_EVENTS)
    assert len(events) == 1
    event = events[0]
    assert event == MOCK_EVENTS[1]

    events = find_events_from_time(datetime(2024, 3, 1, 12, 10, 30), MOCK_EVENTS)
    assert len(events) == 1
    event = events[0]
    assert event == MOCK_EVENTS[2]


def test_find_events_from_time_failure():

    dt = datetime(2024, 12, 1)

    with pytest.raises(HTTPException):
        find_events_from_time(dt, MOCK_EVENTS)


def test_find_events_between_times_failure():

    from_time = datetime(2024, 3, 1, 12, 10, 40)
    to_time = datetime(2024, 3, 1, 12, 10, 50)

    with pytest.raises(HTTPException):
        find_events_between_times(from_time, to_time, MOCK_EVENTS)


def test_find_events_between_times_success():

    # test case 1
    from_time = datetime(2024, 3, 1, 12, 10, 30)
    to_time = datetime(2024, 3, 1, 12, 10, 40)
    expected_result = MOCK_EVENTS[3]

    events = find_events_between_times(from_time, to_time, MOCK_EVENTS)
    assert len(events) == 1

    event = events[0]
    assert event == expected_result

    # test case 2
    from_time = datetime(2024, 1, 1)
    to_time = datetime(2024, 3, 1, 12, 10, 35)
    expected_result = MOCK_EVENTS[1:3]

    events = find_events_between_times(from_time, to_time, MOCK_EVENTS)
    assert len(events) == 2
    assert events == expected_result

    # test case 3 -> no from_time set, looks at event created after today from time 0
    from_time = None
    to_time = datetime(2025, 1, 1)

    dt = datetime.now()
    dt = dt.replace(hour=12, minute=30, second=0, microsecond=0)

    expected_event = Event(id=50, description="test50", time=dt)

    events = find_events_between_times(from_time, to_time, [expected_event])
    assert len(events) == 1
    event = events[0]
    assert event == expected_event
