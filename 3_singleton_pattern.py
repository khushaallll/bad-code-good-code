import os
import threading
from typing import Optional

class MetricsCollector():
    _instance: Optional["MetricsCollector"] = None
    _lock: threading.Lock = threading.Lock()

    def __new__(cls) -> "MetricsCollector":
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        if getattr(self, '_initialized', False):
            return

        self.events: list = []
        self._initialized = True

    def record(self, stage, seconds, rows) -> None:
        self.events.append([stage, seconds, rows])

    def flush(self):
        events = self.events
        self.events = []
        return events

# Called from extract module
collector = MetricsCollector()
collector.record(stage="extract", seconds=4.2, rows=10000)

# Called from transform module
collector = MetricsCollector()
collector.record(stage="transform", seconds=1.8, rows=9950)

all_events = collector.flush()
print(all_events)