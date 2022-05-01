import queue
import time
import weakref
import pytest

from nameserver.cache import TTLCache


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


def test_place_refresh():
    cache = TTLCache(cycleTime=1)

    cache.place('A', 123, 5)

    originalTime = cache.request('A')[0].timeOfDeath

    time.sleep(2)

    afterWaitTime = cache.request('A')[0].timeOfDeath

    assert afterWaitTime == originalTime

    cache.place('A', 123, 100)

    replaceTime = cache.request('A')[0].timeOfDeath

    assert originalTime != replaceTime


@pytest.mark.skip(reason="This is really inconstant and the system is really simple. No way this fails")
def test_polling_replacer():
    cache = TTLCache(1, .1)

    cache.place('A', 1, 9999)
    while True:
        try:
            # trying to place it in the middle of a cache cycle
            cache.place('B', 1, 9999)
        except:
            print("FULLNESS")
            continue

        break

    assert not cache.request('A')[1]

    assert cache.request('B')[1] and cache.request('B')[0].value == 1

    cache.cycleTime = 5

    time.sleep(1)

    cache.place('B', 1, 0)

    cache.cycleTime = .1

    time.sleep(5)

    assert cache.request('A')[1]  # value returned by safety thread


def test_destruction():
    cacheName = "TestName"
    cache = TTLCache(cycleTime=1, name=cacheName)

    ref = weakref.ref(cache)

    del cache

    time.sleep(2)  # to ensure the cleaner thread dies out

    assert ref() == None
