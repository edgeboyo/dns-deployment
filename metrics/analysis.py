

def analyzeDomains(domainList):
    from metrics.consumers import client, bucket

    query_api = client.query_api()
    tables = query_api.query(
        f'from(bucket:"{bucket}") |> range(start: -1w)')

    print(tables)

    return {}
