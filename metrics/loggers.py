import queue

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
        num = (num << 4) + int(seg)
    return num


class ColdAccessLog():
    def __init__(self, secondLevelDomainName, timeOfAccess):
        self.domain = secondLevelDomainName
        self.timeOfAccess = timeOfAccess


class HotAccessLog():
    def __init__(self, secondLevelDomainName, timeOfAccess):
        self.domain = secondLevelDomainName
        self.timeOfAccess = timeOfAccess


class UniqueAccessLog():
    def __init__(self, secondLevelDomainName, timeOfAccess, ip):
        self.domain = secondLevelDomainName
        self.timeOfAccess = timeOfAccess
        self.ip = ipToInt(ip)


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
