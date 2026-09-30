"""A thread-safe pub/sub event bus.

Each subscriber gets its own queue, so N browser tabs each get their own
independent event stream from an SSE endpoint without stepping on each
other — the bus doesn't care how many subscribers there are or when they
connect.
"""
from __future__ import annotations

import queue
import threading
import time
from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass(frozen=True)
class Event:
    agent: str
    type: str  # "thinking" | "message" | "action" | "done"
    payload: str
    ts: float = field(default_factory=time.time)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class EventBus:
    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._subscribers: list[queue.Queue[Event]] = []

    def subscribe(self) -> queue.Queue[Event]:
        q: queue.Queue[Event] = queue.Queue()
        with self._lock:
            self._subscribers.append(q)
        return q

    def unsubscribe(self, q: queue.Queue[Event]) -> None:
        with self._lock:
            if q in self._subscribers:
                self._subscribers.remove(q)

    def publish(self, event: Event) -> None:
        with self._lock:
            subscribers = list(self._subscribers)
        for q in subscribers:
            q.put(event)

    @property
    def subscriber_count(self) -> int:
        with self._lock:
            return len(self._subscribers)
