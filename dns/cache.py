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

        self.exit_flag = False

        thread = threading.Thread(target=self.operate)
        thread.daemon = True
        thread.start()

    def __del__(self):
        # This will likely never be run as the operator thread has info of the cache
        self.exit_flag = True

    def operate(self):
        while True:
            if self.exit_flag:
                print("Leaving gracefully...")
                try:
                    while True:
                        # purging entries for awaiting threads
                        self.strongRefQueue.get(timeout=.1)
                except:
                    return
            try:
                ref = self.strongRefQueue.get_nowait()
                if ref.outOfTimeCheck():
                    self.strongRefQueue.put_nowait(ref)
                    time.sleep(self.cycleTime)

            except queue.Empty as _:
                time.sleep(self.cycleTime)
                continue
            except queue.Full as _:
                # This is done in case of a full error on the outOfTimeCheck. There is no way to peek onto the top of the queue
                # So there is a chance it would get overridden in this time. As such it's better allow this be done via a block
                thread = threading.Thread(
                    target=(lambda: self.strongRefQueue.put(ref)))
                thread.daemon = True
                thread.start()
            except Exception as e:
                print("TTL Queue unexpetced error...")
                traceback.print_exc()
                if self.faultCounter < self.maxFaults:
                    print(
                        f"Adding to fault counter. Currently at {self.faultCounter + 1}")
                    self.faultCounter += 1
                else:
                    raise Exception(
                        f"Reached maximum amount of faults in TTL cache {self.name}")

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

    def close(self):
        self.exit_flag = True


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
