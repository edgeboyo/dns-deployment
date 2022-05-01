import queue

consumerQueue = queue.Queue()


def consumeAccessLog():
    if consumerQueue ==
    return consumerQueue.get()


def ipToInt(ip):
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

    def __place_log(log):
        if not consumerQueue:
            return
        else:
            consumerQueue.put(log)

    def logColdAccess(secondLevelDomainName, timeOfAccess):
        Logger.__place_log(ColdAccessLog(secondLevelDomainName, timeOfAccess))

    def logHotAccess(secondLevelDomainName, timeOfAccess):
        Logger.__place_log(HotAccessLog(secondLevelDomainName, timeOfAccess))

    def logUniqueAccess(secondLevelDomainName, timeOfAccess, ipOfRequester):
        Logger.__place_log(UniqueAccessLog(
            secondLevelDomainName, timeOfAccess, ipOfRequester))
