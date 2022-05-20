

def fetchMetrics(domainList):
    from metrics.consumers import client, bucket

    rawMetrics = {}
    for domain in domainList:
        query_api = client.query_api()

        query = f"""from(bucket:"{bucket}") 
            |> range(start: -1w) 
            |> filter(fn: (r) => r["secondLevelDomain"] == "{domain}")
            |> filter(fn: (r) => r["_measurement"] == "hot_access")
            |> sum()"""

        # print(query)

        hotAccess = query_api.query(query)

        hotAccessValue = 0
        for table in hotAccess:
            for row in table.records:
                # print(row.values)
                hotAccessValue = max(hotAccessValue, row.values['_value'])

        print(f"Domain {domain} has a hot access of {hotAccessValue}")

        query = f"""from(bucket:"{bucket}") 
            |> range(start: -1w) 
            |> filter(fn: (r) => r["secondLevelDomain"] == "{domain}")
            |> filter(fn: (r) => r["_measurement"] == "cold_access")
            |> sum()"""

        # print(query)

        coldAccess = query_api.query(query)

        coldAccessValue = 0
        for table in coldAccess:
            for row in table.records:
                # print(row.values)
                coldAccessValue = max(coldAccessValue, row.values['_value'])

        print(f"Domain {domain} has a cold access of {coldAccessValue}")

        query = f"""from(bucket:"{bucket}") 
            |> range(start: -1w) 
            |> filter(fn: (r) => r["secondLevelDomain"] == "{domain}")
            |> filter(fn: (r) => r["_measurement"] == "unique_access")
            |> distinct()"""

        uniqueAccess = query_api.query(query)

        uniqueAccessValue = 0
        for table in uniqueAccess:
            uniqueAccessValue = max(uniqueAccessValue, len(table.records))
            for row in table.records:
                pass
                # print(row.values)

        print(f"Domain {domain} has a unique access of {uniqueAccessValue}")

        rawMetrics[domain] = (
            hotAccessValue, coldAccessValue, uniqueAccessValue)

    return rawMetrics


def processMetrics(metrics):
    scores = {}

    # Hot Access Ranking
    hotRank = []

    # Cold Access Ranking
    coldRank = []

    # Unique Access Ranking
    uniqueRank = []

    # Proportion of hot to cold
    propRank = []

    for domain, values in metrics.items():
        scores[domain] = 0

        (hot, cold, unique) = values

        # Add all rankings onto lists
        hotRank.append((hot, domain))
        coldRank.append((cold, domain))
        uniqueRank.append((unique, domain))
        propRank.append((hot / cold if cold != 0 else 0, domain))

    # Sort values from
    hotRank.sort()
    coldRank.sort()
    uniqueRank.sort()
    propRank.sort()

    # Get top of each ranking
    # Exact number can be tweaked
    hotRank = reversed(hotRank[-5:])
    coldRank = reversed(coldRank[-5:])
    uniqueRank = reversed(uniqueRank[-5:])
    propRank = reversed(propRank[-5:])

    # These stater values can be tweaked
    # They decrement by a certain amount with each iteration
    uniqueStarter = 6
    for rank in uniqueRank:
        (_, domain) = rank
        scores[domain] += max(uniqueStarter, 0)
        uniqueStarter -= 1

    propStarter = 3
    for rank in propRank:
        (_, domain) = rank
        scores[domain] += max(propStarter, 0)
        propStarter -= 1

    coldStarter = 2
    for rank in coldRank:
        (_, domain) = rank
        scores[domain] += max(coldStarter, 0)
        coldStarter -= 1

    hotStarter = 2
    for rank in hotRank:
        (_, domain) = rank
        scores[domain] += max(hotStarter, 0)
        hotStarter -= 1

    return scores
