import pytest
from pydantic import ValidationError

from day_12 import LRUCache  # Change this if your filename differs


def test_missing_key_returns_none():
    cache = LRUCache(capacity=2)

    assert cache.get("missing") is None


def test_get_existing_key():
    cache = LRUCache(capacity=2)
    cache.put("A", "alpha")

    assert cache.get("A") == "alpha"


def test_get_updates_recency_and_evicts_lru():
    cache = LRUCache(capacity=2)
    cache.put("A", "alpha")
    cache.put("B", "beta")

    assert cache.get("A") == "alpha"  # A becomes most recently used

    cache.put("C", "gamma")  # B should be evicted

    assert cache.get("B") is None
    assert cache.get("A") == "alpha"
    assert cache.get("C") == "gamma"


def test_updating_existing_key_does_not_evict_other_key():
    cache = LRUCache(capacity=2)
    cache.put("A", "alpha")
    cache.put("B", "beta")

    result = cache.put("A", "updated-alpha")

    assert result is None
    assert cache.get("A") == "updated-alpha"
    assert cache.get("B") == "beta"


def test_updating_key_changes_recency():
    cache = LRUCache(capacity=2)
    cache.put("A", "alpha")
    cache.put("B", "beta")

    cache.put("A", "updated-alpha")
    cache.put("C", "gamma")

    assert cache.get("B") is None
    assert cache.get("A") == "updated-alpha"
    assert cache.get("C") == "gamma"


def test_capacity_one():
    cache = LRUCache(capacity=1)

    cache.put("A", "alpha")
    cache.put("B", "beta")

    assert cache.get("A") is None
    assert cache.get("B") == "beta"


@pytest.mark.parametrize("capacity", [0, -1, True, False, 1.5, "2"])
def test_invalid_capacity_is_rejected(capacity):
    with pytest.raises(ValidationError):
        LRUCache(capacity=capacity)


def test_put_returns_none():
    cache = LRUCache(capacity=2)

    assert cache.put("A", "alpha") is None