# Multi-Agent Visual Sandbox

A small multi-agent simulation (Researcher → Planner → Executor → Critic)
that streams its internal events live to a browser over Server-Sent Events,
with a real-time visualization of who's doing what as it happens — no
polling, no page refresh.

## What this demonstrates

- **A real event bus**, not a mock: `sandbox/bus.py` is a thread-safe
  pub/sub broker. Each agent runs on its own thread and publishes typed
  events (`thinking`, `message`, `action`, `done`) as it works; any number
  of browser tabs can subscribe independently and each gets its own event
  stream from the moment it connects.
- **Real-time streaming over plain HTTP**: Server-Sent Events instead of
  WebSockets — deliberately, since this is one-directional (server →
  browser) event streaming and SSE needs no extra dependencies, reconnects
  automatically in the browser, and is trivial to curl and inspect
  (`curl localhost:5000/events`) while debugging.
- **A live visualization with no framework**: `static/app.js` is ~100 lines
  of vanilla JS driving a CSS-animated node graph — agent nodes light up as
  they act, with a scrolling event log underneath.

## Run it

```bash
pip install -r requirements.txt
python -m sandbox.app
# open http://localhost:5000
```

Refresh the page (or open a second tab) to start a new simulation run —
each connection gets a fresh set of agents working through a new task.

## Layout

```
sandbox/
  agents.py     the 4 simulated agents + the task loop each runs
  bus.py        thread-safe pub/sub event bus
  app.py        Flask app: SSE endpoint + static page
static/
  index.html     visualization page
  app.js         EventSource client + node-graph rendering
tests/
  test_bus.py           event bus pub/sub correctness
  test_agents.py        agents emit well-formed, ordered events
```

## Stack

Python · Flask · Server-Sent Events · vanilla JS/CSS · unittest
