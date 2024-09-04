from utils.models import Event
from datetime import datetime

MOCK_EVENTS = [
    Event(id=1, description="test1", time=datetime(2024, 1, 1)),
    Event(id=2, description="test2", time=datetime(2024, 2, 1)),
    Event(id=3, description="test3", time=datetime(2024, 3, 1, 12, 10, 30)),
    Event(id=4, description="test4", time=datetime(2024, 3, 1, 12, 10, 35)),
    Event(id=5, description="test5", time=datetime(2024, 3, 1, 12, 10, 40)),
]
