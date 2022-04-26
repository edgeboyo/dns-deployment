from ast import keyword
import queue
import threading
import time
import traceback
import weakref


class TTLCache():
    def __init__(self, maxEntries=1000, cycleTime=10, *, name="TTLCache", maxFaults=1):
        self.name = name  # This is for debugging purposes mostly
        self.cycleTime = cycleTime

        self.strongRefQueue = queue.PriorityQueue(maxEntries)
        self.weakRefDict = weakref.WeakValueDictionary()

        self.maxFaults = maxFaults
        self.faultCounter = 0

        thread = threading.Thread(target=operate, args=(weakref.ref(self), ))
        thread.daemon = True
        thread.start()

    def request(self, keyword):
        try:
            result = self.weakRefDict[keyword]
        except:
            return (None, False)

        return (result, result != None)

    def place(self, keyword, newValue, ttl):
        (entry, result) = self.request(keyword)

        if result:
            entry.refreshTTL(newValue, ttl)
        else:
            entry = Entry(keyword, newValue, ttl)

            self.strongRefQueue.put_nowait(entry)
            self.weakRefDict[keyword] = entry


def operate(weakRef):
    while True:
        cache: TTLCache = weakRef()  # create strong reference
        if not cache:
            return
        try:
            ref = cache.strongRefQueue.get_nowait()
            if ref.outOfTimeCheck():
                cache.strongRefQueue.put_nowait(ref)
                time.sleep(cache.cycleTime)

        except queue.Empty as _:
            time.sleep(cache.cycleTime)
        except queue.Full as _:
            # This is done in case of a full error on the outOfTimeCheck. There is no way to peek onto the top of the queue
            # So there is a chance it would get overridden in this time. As such it's better allow this be done via a block
            strongRefQueue = cache.strongRefQueue
            thread = threading.Thread(
                target=(lambda: strongRefQueue.put(ref)))
            thread.daemon = True
            thread.start()
        except Exception as e:
            if cache == None:
                return  # leaving
            print("TTL Queue unexpetced error...")
            traceback.print_exc()
            if cache.faultCounter < cache.maxFaults:
                print(
                    f"Adding to fault counter. Currently at {cache.faultCounter + 1}")
                cache.faultCounter += 1
            else:
                raise Exception(
                    f"Reached maximum amount of faults in TTL cache {cache.name}")

        del cache  # remove strong reference


class Entry():
    def __init__(self, keyword, value, ttl=60):
        self.keyword = keyword
        self.value = value
        self.ttl = ttl
        self.timeOfDeath = time.time() + ttl

    def __str__(self):
        return f"Entry {self.keyword} alive for {self.timeOfDeath - time.time()} [{self.timeOfDeath - time.time() <= 0}]"

    def __lt__(self, entry):
        return self.timeOfDeath < entry.timeOfDeath

    def refreshTTL(self, ttl=None, newObject=None):
        if ttl == None:
            ttl = self.ttl

        self.timeOfDeath = time.time() + ttl

        if newObject != None:
            self.value = newObject

    def outOfTimeCheck(self, now=None):
        now = time.time() if now == None else now
        return not self.timeOfDeath - now <= 0
