# stdlib
from unittest.mock import patch

# deps
import pytest

# local
from src.event_subscription import (
    WatchList,
    has_min_confirmations,
    is_transaction_successfull,
)

from .fixtures import *


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


@pytest.mark.parametrize(
    "mock_get_transaction, expected",
    [({"status": 1}, True), ({"status": 0}, False), (None, False)],
    indirect=["mock_get_transaction"],
)
def test_is_transaction_successfull(mock_get_transaction, expected):
    res = is_transaction_successfull("fake_tx")
    assert res == expected


@pytest.mark.parametrize(
    "mock_min_confirmation_env, mock_get_transaction, mock_transaction_is_successful, expected",
    [
        ("3", {"status": 1}, True, True),
        ("10", {"status": 1}, True, False),
        ("3", {"status": 1}, False, False),
    ],
    indirect=[
        "mock_min_confirmation_env",
        "mock_get_transaction",
        "mock_transaction_is_successful",
    ],
)
@patch("src.event_subscription.w3.eth")
def test_has_min_confirmations(
    mock_eth,
    mock_min_confirmation_env,
    mock_get_transaction,
    expected,
    mock_transaction_is_successful,
):
    mock_eth.block_number = 4
    min_conf = has_min_confirmations(1, "fake-hash")
    assert min_conf == expected
