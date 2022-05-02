import queue

from objects.utils import stampToISO

consumerQueue = queue.Queue()


def disableMetrics():
    global consumerQueue
    consumerQueue = None


def checkMetrics():
    return bool(consumerQueue)


def consumeAccessLog():
    return consumerQueue.get()


def ipToInt(ip: str):
    num = 0
    for seg in ip.split('.'):
        num = (num << 8) + int(seg)
    return num


def intToIP(num: int):
    segments = []
    for _ in range(4):
        seg = str(num % 256)
        num >>= 8
        segments.append(seg)

    if num != 0:
        print(segments)
        print(num)
        raise Exception("IP couldn't be converted back to string")

    return ".".join(reversed(segments))


class ColdAccessLog():
    def __init__(self, secondLevelDomainName, timeOfAccess):
        self.domain = secondLevelDomainName
        self.timeOfAccess = timeOfAccess

    def __str__(self):
        print(
            f"Logged COLD access on {stampToISO(self.timeOfAccess)} to {self.domain}")


class HotAccessLog():
    def __init__(self, secondLevelDomainName, timeOfAccess):
        self.domain = secondLevelDomainName
        self.timeOfAccess = timeOfAccess

    def __str__(self):
        return f"Logged HOT access on {stampToISO(self.timeOfAccess)} to {self.domain}"


class UniqueAccessLog():
    def __init__(self, secondLevelDomainName, timeOfAccess, ip):
        self.domain = secondLevelDomainName
        self.timeOfAccess = timeOfAccess
        self.ip = ipToInt(ip)

    def __str__(self):
        return f"Logged UNIQUE access from {intToIP(self.ip)} on {stampToISO(self.timeOfAccess)} to {self.domain}"


class Logger():
    def __init__(self):
        pass

    def __place_log__(log):
        if not consumerQueue:
            return
        else:
            consumerQueue.put(log)

    def logColdAccess(secondLevelDomainName, timeOfAccess):
        Logger.__place_log__(ColdAccessLog(
            secondLevelDomainName, timeOfAccess))

    def logHotAccess(secondLevelDomainName, timeOfAccess):
        Logger.__place_log__(HotAccessLog(secondLevelDomainName, timeOfAccess))

    def logUniqueAccess(secondLevelDomainName, timeOfAccess, ipOfRequester):
        Logger.__place_log__(UniqueAccessLog(
            secondLevelDomainName, timeOfAccess, ipOfRequester))
