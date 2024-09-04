from fastapi.testclient import TestClient
from utils.main import app
from datetime import datetime, timedelta

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome To Amin's Calendar API :)"}


def test_create_event_success():
    payload = {"description": "first", "time": "2024-01-01T00:00:00", "id": 1}
    response = client.post("/events", json=payload)
    assert response.status_code == 200
    assert response.json() == [payload]


def create_events():
    """creates events in client to be used in tests"""
    payloads = [
        {"description": "first", "time": "2024-01-01T00:00:00", "id": 1},
        {"description": "second", "time": "2024-02-01", "id": 2},
        {"description": "third", "time": "2024-03-01", "id": 3},
        {"description": "fourth", "time": "2024-04-01", "id": 4},
    ]

    for payload in payloads:
        client.post("/events", json=payload)


def test_create_event_failure():
    # test case 1 -> incorrect datetime passed
    payload = {"description": "first", "time": "01-01-2024T00:00:00", "id": 1}
    response = client.post("/events", json=payload)
    assert response.status_code == 422

    # test case 2 -> id already taken
    create_events()
    payload = {"description": "first", "time": "2024-01-01T00:00:00", "id": 1}
    response = client.post("/events", json=payload)
    assert response.status_code == 400
    assert response.json() == {
        "detail": "id=1 has already been taken, please use a different id"
    }


def test_get_event_from_id_success():
    create_events()
    expected_event = {"description": "first", "time": "2024-01-01T00:00:00", "id": 1}
    response = client.get(f"/events/{expected_event['id']}")
    assert response.status_code == 200
    assert response.json() == expected_event


def test_get_event_from_id_failure():
    create_events()
    event_id = 10
    response = client.get(f"/events/{event_id}")
    assert response.status_code == 404
    assert response.json() == {"detail": f"events with id {event_id} not found"}


def test_get_event_from_time_success():
    create_events()
    time = "2024-01-01T00:00:00"
    expected_result = {"description": "first", "time": time, "id": 1}

    response = client.get("/events?datetime_format=2024-01-01")
    assert response.status_code == 200
    assert response.json() == [expected_result]


def test_get_event_from_time_failure():
    create_events()
    time = "2025-01-01T00:00:00"

    response = client.get(f"/events?datetime_format={time}")
    assert response.status_code == 404
    assert response.json() == {
        "detail": "events with time 2025-01-01 00:00:00 not found"
    }


def test_get_events_all_events_returned():
    create_events()

    expected_result = [
        {"description": "first", "time": "2024-01-01T00:00:00", "id": 1},
        {"description": "second", "time": "2024-02-01T00:00:00", "id": 2},
        {"description": "third", "time": "2024-03-01T00:00:00", "id": 3},
        {"description": "fourth", "time": "2024-04-01T00:00:00", "id": 4},
    ]

    response = client.get("/events")
    assert response.status_code == 200
    assert response.json() == expected_result


def test_get_events_between_times_success():
    create_events()

    # test case 1 -> from_time and to_time provided
    from_time = "2024-01-01"
    to_time = "2024-04-01"

    response = client.get(f"/events?from_time={from_time}&to_time={to_time}")
    assert response.status_code == 200
    assert len(response.json()) == 2
    assert response.json() == [
        {"description": "second", "time": "2024-02-01T00:00:00", "id": 2},
        {"description": "third", "time": "2024-03-01T00:00:00", "id": 3},
    ]

    # test case 2 -> no from_time set
    # create a event with a future date, this should be returned
    to_time = datetime.now() + timedelta(days=60)
    to_time_str = to_time.strftime("%Y-%m-%d")

    future_date = datetime.now() + timedelta(days=30)
    future_date_str = future_date.strftime("%Y-%m-%d")

    new_event = {"description": "test", "time": future_date_str, "id": 1000}
    client.post("/events", json=new_event)

    response = client.get(f"/events?to_time={to_time_str}")
    assert response.status_code == 200
    assert len(response.json()) == 1

    result = response.json()[0]
    assert result["id"] == new_event["id"]
    assert result["description"] == new_event["description"]


def test_get_events_between_times_failure():
    create_events()

    # test case 1 -> from_time and to_time provided
    from_time = "2024-04-01"
    to_time = "2024-05-01"

    response = client.get(f"/events?from_time={from_time}&to_time={to_time}")
    assert response.status_code == 404
    assert response.json() == {
        "detail": "no events found between times 2024-04-01 00:00:00 and 2024-05-01 00:00:00"
    }
