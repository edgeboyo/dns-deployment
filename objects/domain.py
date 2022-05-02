import json
import os
import time

from objects.io import fetchDomainFile, listDomainNames, runSSGA
from objects.records import interpretRecord, validateRecord, supportedRecords
from objects.utils import stampToISO

tld = None


def setTopLevelDomain(topLevelDomain):
    global tld

    if not topLevelDomain.isalpha():
        raise Exception(
            f"{topLevelDomain} contains non letter chars. TLD needs to only contain chars")

    tld = topLevelDomain


# get TLD of the system
def getLocalTLD():
    return tld


def createNewDomain(domainName):
    now = time.time()

    allowedInDomainName = [chr(c)
                           for c in range(ord('a'), ord('z') + 1)] + ['-']
    if domainName[0] == '-' or domainName[-1] == '-' or any(map(lambda c: c not in allowedInDomainName, domainName)):
        raise Exception(
            f"Domain name {domainName} contains invalid characters or has a '-' char on either end")

    domain = {"domainName": domainName, "records": {},
              "registeredAt": stampToISO(now)}

    for record in supportedRecords:
        domain['records'][record] = []

    domain['ssgaResult'] = runSSGA(f"{domainName}.{tld}")

    with open(fetchDomainFile(domainName, True), "w") as f:
        json.dump(domain, f, indent=4)

    return domain


def fetchDomain(domainName):
    with open(fetchDomainFile(domainName)) as f:
        return json.load(f)


def deleteDomain(domainName):
    domainFile = fetchDomainFile(domainName)

    os.remove(domainFile)


def fetchAllDomainNames():
    return listDomainNames()


def overrideRecords(domainName, recordType, records):
    if recordType not in supportedRecords:
        raise Exception(f"`{recordType} is not supported record type")

    # this raises errors if validation fails
    records = validateRecord(recordType, records)

    # in case of rewrites to other records do read white in one go
    with open(fetchDomainFile(domainName), "r+") as f:
        domain = json.load(f)

        f.truncate(0)
        f.seek(0)

        domain['records'][recordType] = records

        json.dump(domain, f, indent=4)

    return records


def checkTLD(domainName: str):
    return domainName.endswith("." + tld) or domainName.endswith("." + tld + ".")

# Get second level domain of local deployment


def getNthLevelDomain(domainName, level):
    encounteredTLD = False
    secondLevel = None

    segments = list(reversed(domainName.split('.')))

    if len(segments[0]) == 0:
        del segments[0]

    for i, segment in enumerate(segments):
        if len(segments) == 0:
            raise Exception(
                f"Misshapen domain lookup. Encountered empty domain level {i + 1} in {domainName}")
        elif i + 1 == level:
            return segment

    raise Exception(
        f"Domain name {domainName} does not have a {level} level domain")


def requestRecords(domainName: str):
    secondLevel = getNthLevelDomain(domainName, 2)
    if secondLevel == None:
        return {}

    try:
        domain = fetchDomain(secondLevel)
    except:
        return {}

    records = interpretRecord(domain['records'], secondLevel, tld)

    return records
