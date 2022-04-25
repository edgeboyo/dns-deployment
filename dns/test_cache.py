import queue
import time
import pytest

from dns.cache import TTLCache


def test_simple_queue():
    cache = TTLCache(cycleTime=1)
    values = list(range(0, 100))

    ttl = 6

    for val in values:
        cache.place(str(val), val, ttl)

    cmp, _ = cache.request('5')

    cmp = cmp.value

    time.sleep(5)

    entry, wasFound = cache.request('5')

    assert wasFound

    assert cmp == entry.value

    del entry

    time.sleep(5)

    entry, wasFound = cache.request('5')

    assert not wasFound

    assert entry == None


def test_fullness_exception():
    with pytest.raises(queue.Full) as _:
        cache = TTLCache(99, 999)
        for i in range(0, 100):
            cache.place(str(i), i, 100)
