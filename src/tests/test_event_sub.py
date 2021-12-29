# deps
import pytest

# local
from src.event_subscription import WatchList


class TestWatchList:
    def test_subscribe(self):
        wl = WatchList()
        wl.subscribe("fake-address")

        assert "fake-address" in wl._subscribers

    def test_unsubscribe(self):
        wl = WatchList()
        wl._subscribers = ["fake-address"]
        assert "fake-address" in wl._subscribers
        wl.unsubscribe("fake-address")
        assert "fake-address" not in wl._subscribers

    def test_is_subscribed(self):
        wl = WatchList()
        wl._subscribers = ["fake-address"]

        assert wl.is_subscribed("fake-address")

    def test_get_subscribers(self):
        wl = WatchList()
        wl._subscribers = ["fake-address"]

        subs = wl.get_subscribers()
        assert subs == wl._subscribers
        assert subs is not wl._subscribers


# def test_is_transaction_successfull(self):
#    pass

# def test_has_min_confirmations(self):
#    pass
