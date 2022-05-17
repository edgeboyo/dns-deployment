import traceback

from flask import Flask, request, send_from_directory

from flask_cors import CORS
from metrics.analysis import analyzeDomains

from objects.domain import createNewDomain, deleteDomain, fetchAllDomainNames, fetchDomain, findSimilarDomains, overrideRecords

from api.returns import return_json, return_error

app = Flask(__name__)
CORS(app)


@app.route("/")
def gui_root():
    return gui_files('index.html')


@app.route("/<path:path>")
def gui_files(path):
    try:
        return send_from_directory('../frontend', path)
    except:
        traceback.print_exc()
        raise


@app.route("/api")
def api_root():
    from objects.domain import tld
    data = {"topLevelDomain": f".{tld}",
            "domains": "/api/domains",
            "analyzer": "/api/analyze"}
    return return_json(data)


@app.route("/api/domains", methods=['GET'])
def api_domains_get():
    from objects.domain import tld
    domains = []
    for domainName in fetchAllDomainNames():
        domain = {"domainName": domainName,
                  "resource": f"/api/domains/{domainName}", "uri": f"{domainName}.{tld}", "records": f"/api/domains/{domainName}/records"}

        domains.append(domain)

    return return_json(domains)


@app.route("/api/domains", methods=['POST'])
def api_domains_post():
    from objects.domain import tld
    if not request.is_json:
        return return_error("Data not formatted as JSON")

    data = request.get_json()

    domainName = data['domainName']

    if not domainName:
        return return_error("`domainName` field missing in request")

    try:
        createNewDomain(domainName)
    except Exception as e:
        return return_error(str(e), 409)

    domain = {"domainName": domainName,
              "resource": f"/api/domains/{domainName}", "uri": f"{domainName}.{tld}", "records": f"/api/domains/{domainName}/records"}

    return return_json(domain)


@app.route("/api/domains/<domainName>", methods=["GET"])
def api_domain_details(domainName):
    try:
        domain = fetchDomain(domainName)
    except Exception as e:
        return return_error(str(e), 404)

    domain['records'] = f'/api/domains/{domainName}/records'

    return return_json(domain)


@app.route("/api/domains/<domainName>", methods=["DELETE"])
def api_delete_domain(domainName):
    try:
        deleteDomain(domainName)
    except Exception as e:
        return return_error(str(e), 404)

    return return_json({"message": "Domain removed"})


@app.route("/api/domains/<domainName>/records", methods=["GET"])
def api_domain_records(domainName):
    try:
        domain = fetchDomain(domainName)
    except Exception as e:
        return return_error(str(e), 404)

    records = domain['records']

    for type, recs in records.items():
        records[type] = {
            "records": f"/api/domains/{domainName}/records/{type.lower()}", "amount": len(recs)}

    return return_json(records)


@app.route("/api/domains/<domainName>/records/<recordType>", methods=["GET"])
def api_domain_records_specific(domainName, recordType):
    try:
        domain = fetchDomain(domainName)
    except Exception as e:
        return return_error(str(e), 404)

    recordType = recordType.upper()

    records = domain['records']

    if recordType not in records:
        return return_error(f"{recordType.upper()} is not a valid record type")

    return return_json(records[recordType])


@app.route("/api/domains/<domainName>/records/<recordType>", methods=["PUT", "PATCH"])
def api_domain_records_change(domainName, recordType):
    if not request.is_json:
        return return_error("Data not formatted as JSON")

    data = request.get_json()

    if not isinstance(data, list):
        return return_error("Request body must be list of records")

    recordType = recordType.upper()

    try:
        # for now to PUT/PATCH the same, think of how to do it differently
        records = overrideRecords(domainName, recordType, data)
    except Exception as e:
        # traceback.print_exc()
        return return_error(str(e))

    return return_json(records)


@app.route("/api/analyze", methods=["GET"])
def api_analyze():
    arguments = request.args.to_dict()

    required = {'domain': "Input domain you want to analyze",
                'similarity': "Input the threshold of similarity (per 5 characters rounded up)"}

    for field, desc in required.items():
        if field not in arguments:
            return return_error(f"{desc} as `{field}` field in your query parameters")

    try:
        analysisResults = findSimilarDomains(**arguments)
        analysisResults[arguments['domain']] = 0
        print(analysisResults)
        (metricsResults, raw) = analyzeDomains(list(analysisResults.keys()))
    except Exception as e:
        traceback.print_exc()
        return return_error(str(e), 404)

    # Encode metrics in a more readable way
    for domain, similarity in analysisResults.items():
        (hot, cold, unique) = raw[domain]
        raw[domain] = {}
        raw[domain]['hot'] = hot
        raw[domain]['cold'] = cold
        raw[domain]['unique'] = unique
        raw[domain]['deviation'] = similarity

    computedObject = {"originalityScores": metricsResults, "rawMetrics": raw}

    return return_json(computedObject)
