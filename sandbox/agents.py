"""Four simulated agents that hand a task off in sequence, each publishing
events to the bus as they work. The "work" is scripted/simulated (sleeps +
canned reasoning strings) rather than calling a real LLM, so a run is fast,
free, and deterministic to watch — the event-bus and streaming plumbing
around it is the real part of this demo.
"""
from __future__ import annotations

import random
import threading
import time

from sandbox.bus import Event, EventBus

_TASKS = [
    "summarize last week's support tickets",
    "draft a release-notes outline",
    "triage the open bug backlog",
]


def _researcher(bus: EventBus, task: str) -> str:
    bus.publish(Event("researcher", "thinking", f"Gathering context for: {task}"))
    time.sleep(random.uniform(0.4, 0.8))
    findings = f"Found 3 relevant sources for '{task}'."
    bus.publish(Event("researcher", "message", findings))
    return findings


def _planner(bus: EventBus, task: str, findings: str) -> str:
    bus.publish(Event("planner", "thinking", "Breaking task into steps"))
    time.sleep(random.uniform(0.4, 0.8))
    plan = f"Plan: (1) review sources, (2) draft, (3) self-check. Based on: {findings}"
    bus.publish(Event("planner", "message", plan))
    return plan


def _executor(bus: EventBus, plan: str) -> str:
    bus.publish(Event("executor", "action", "Executing plan step 1/3"))
    time.sleep(random.uniform(0.3, 0.6))
    bus.publish(Event("executor", "action", "Executing plan step 2/3"))
    time.sleep(random.uniform(0.3, 0.6))
    bus.publish(Event("executor", "action", "Executing plan step 3/3"))
    time.sleep(random.uniform(0.3, 0.6))
    output = "Draft produced."
    bus.publish(Event("executor", "message", output))
    return output


def _critic(bus: EventBus, output: str) -> None:
    bus.publish(Event("critic", "thinking", f"Reviewing: {output}"))
    time.sleep(random.uniform(0.3, 0.6))
    verdict = "Looks good — no revisions needed." if random.random() > 0.3 else (
        "Needs one revision: tighten the summary."
    )
    bus.publish(Event("critic", "message", verdict))
    bus.publish(Event("critic", "done", "Run complete."))


def run_simulation(bus: EventBus) -> None:
    """Runs one full agent hand-off chain, publishing events as it goes.
    Intended to be started on its own thread per browser connection.
    """
    task = random.choice(_TASKS)
    bus.publish(Event("system", "message", f"New task: {task}"))

    findings = _researcher(bus, task)
    plan = _planner(bus, task, findings)
    output = _executor(bus, plan)
    _critic(bus, output)


def run_simulation_in_background(bus: EventBus) -> threading.Thread:
    t = threading.Thread(target=run_simulation, args=(bus,), daemon=True)
    t.start()
    return t
