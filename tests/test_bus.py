import unittest

from sandbox.bus import Event, EventBus


class EventBusTests(unittest.TestCase):
    def test_subscriber_receives_published_event(self):
        bus = EventBus()
        q = bus.subscribe()
        event = Event(agent="researcher", type="thinking", payload="hi")
        bus.publish(event)
        received = q.get(timeout=1)
        self.assertEqual(received, event)

    def test_multiple_subscribers_each_get_their_own_copy(self):
        bus = EventBus()
        q1 = bus.subscribe()
        q2 = bus.subscribe()
        event = Event(agent="planner", type="message", payload="plan")
        bus.publish(event)
        self.assertEqual(q1.get(timeout=1), event)
        self.assertEqual(q2.get(timeout=1), event)

    def test_unsubscribe_stops_delivery(self):
        bus = EventBus()
        q = bus.subscribe()
        bus.unsubscribe(q)
        bus.publish(Event(agent="critic", type="message", payload="done"))
        self.assertTrue(q.empty())

    def test_subscriber_count(self):
        bus = EventBus()
        self.assertEqual(bus.subscriber_count, 0)
        q = bus.subscribe()
        self.assertEqual(bus.subscriber_count, 1)
        bus.unsubscribe(q)
        self.assertEqual(bus.subscriber_count, 0)


if __name__ == "__main__":
    unittest.main()
