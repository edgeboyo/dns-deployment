import json
import time

from objects.io import fetchDomainFile, listDomainNames
from objects.utils import stampToISO


def createNewDomain(domainName):
    now = time.time()
    domain = {"domainName": domainName, "records": {},
              "registeredAt": stampToISO(now)}

    records = ['A', 'AAAA', 'CNAME', 'TXT']

    for record in records:
        domain['records'][record] = []

    with open(fetchDomainFile(domainName), "w") as f:
        json.dump(domain, f, indent=4)

    return domain


def fetchAllDomainNames():
    return listDomainNames()
