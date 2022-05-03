from threading import Thread
import time
import requests
import random
from typoGenerator import createDerivations
import dns.resolver

uri = '127.0.0.1'


def createDomain(dn):
    obj = {
        "domainName": dn
    }

    records = [{"hostname": "@", "mapping": "127.0.0.1",
                "ttl": random.randrange(5, 15)}]

    r = requests.post(f'http://{uri}/api/domains', json=obj)

    print(r.text)

    r = requests.put(
        f'http://{uri}/api/domains/{dn}/records/a', json=records)

    print(r.text)


def performCalls(domain, amount):
    while amount > 0:
        resolver = dns.resolver.Resolver()
        resolver.nameservers = [uri]

        try:
            resolver.resolve(domain + ".com")
        except:
            pass  # Some errors are expected in a stress test like this

        amount -= 1
        time.sleep(random.randint(1, 2))


validDomains = ['google', 'facebook', 'southampton']

calls = {}
for dn in validDomains:
    createDomain(dn)
    calls[dn] = 500
    for der in createDerivations(dn + '.com', 5):
        der = der.split('.')[0]
        if der not in calls:
            createDomain(der)
            calls[der] = random.randint(50, 100)

threads = []
for dn, calls in calls.items():
    thread = Thread(target=performCalls, args=(dn, calls))
    thread.daemon = True
    thread.start()

    threads.append(thread)

# Wait for all the calls to finish
for thread in threads:
    thread.join()

print("Stress test finished. Running analysis")

# Get analyzer results
for dn in validDomains:
    obj = {
        'domain': dn,
        'similarity': 2 if len(dn) <= 6 else 3
    }

    r = requests.get(f'http://{uri}/api/analyze', params=obj)

    print("Analyzer for " + dn + ": ")
    print(r.text)

# print("Stress test finished")
