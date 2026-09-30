"""Flask app: serves the visualization page and streams agent events over
Server-Sent Events.
"""
from __future__ import annotations

import json
import os
import queue

from flask import Flask, Response, send_from_directory

from sandbox.agents import run_simulation_in_background
from sandbox.bus import EventBus

STATIC_DIR = os.path.join(os.path.dirname(__file__), "..", "static")

app = Flask(__name__, static_folder=None)


@app.route("/")
def index():
    return send_from_directory(STATIC_DIR, "index.html")


@app.route("/static/<path:filename>")
def static_files(filename):
    return send_from_directory(STATIC_DIR, filename)


@app.route("/events")
def events():
    bus = EventBus()
    q = bus.subscribe()
    run_simulation_in_background(bus)

    def stream():
        try:
            while True:
                event = q.get(timeout=30)
                yield f"data: {json.dumps(event.to_dict())}\n\n"
                if event.type == "done":
                    break
        except queue.Empty:
            yield "event: timeout\ndata: {}\n\n"
        finally:
            bus.unsubscribe(q)

    return Response(stream(), mimetype="text/event-stream")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, threaded=True)
