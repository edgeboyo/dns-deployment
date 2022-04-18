import json


def createDomain(domainName):
    domain = {"domainName": domainName, "records": {}}

    records = ['A', 'AAAA', 'CNAME', 'TXT']

    for record in records:
        domain['records'][record] = {}

    return domain


def fetchAllDomains():
    pass
