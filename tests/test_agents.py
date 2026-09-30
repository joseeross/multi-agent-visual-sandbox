import unittest

from sandbox.agents import run_simulation
from sandbox.bus import EventBus

EXPECTED_AGENTS_IN_ORDER = ["system", "researcher", "planner", "executor", "critic"]


class AgentSimulationTests(unittest.TestCase):
    def test_run_simulation_emits_events_from_every_agent_in_order(self):
        bus = EventBus()
        q = bus.subscribe()
        run_simulation(bus)  # runs synchronously on the calling thread

        events = []
        while not q.empty():
            events.append(q.get_nowait())

        self.assertGreater(len(events), 0)
        seen_agents_in_order = []
        for e in events:
            if not seen_agents_in_order or seen_agents_in_order[-1] != e.agent:
                seen_agents_in_order.append(e.agent)
        self.assertEqual(seen_agents_in_order, EXPECTED_AGENTS_IN_ORDER)

    def test_last_event_is_done(self):
        bus = EventBus()
        q = bus.subscribe()
        run_simulation(bus)

        events = []
        while not q.empty():
            events.append(q.get_nowait())

        self.assertEqual(events[-1].type, "done")
        self.assertEqual(events[-1].agent, "critic")


if __name__ == "__main__":
    unittest.main()
