import os
import json
from flask import Flask, request

from .returns import return_json, return_error

tld = "tld"  # will be imported from config later

app = Flask(__name__)

# ROUTINGS BEGIN HERE


@app.route("/")
def gui_root():
    return "<p>This will be the GUI root later</p>"


@app.route("/api")
def api_root():
    data = {"documentation": "/api/docs",
            "topLevelDomain": f".{tld}", "domains": "/api/domains"}
    return return_json(data)


@app.route("/api/domains", methods=['GET'])
def api_domains_get():
    domains = []
    for file in os.listdir('./data'):
        if not os.fsdecode(file).endswith('.json'):
            continue

        filePath = f"./data/{file}"

        with open(filePath) as f:
            domainInfo = json.load(f)
            domainName = domainInfo['domainName']

        domain = {"domainName": domainName,
                  "resource": f"/api/domains/{domainName}", "uri": f"{domainName}.{tld}", "records": f"/api/domains/{domainName}/records"}

        domains.append(domain)

    return return_json(domains)


@app.route("/api/domains", methods=['POST'])
def api_domains_post():
    print("AAAAAAAAAAAAAAAAAAAAA")

    if not request.is_json:
        return return_error("Data not formatted as JSON")

    data = request.get_json()

    domainName = data['domainName']

    if not domainName:
        return return_error("`domainName` field missing in request")

    filePath = f"./data/{domainName}.json"

    if os.path.exists(filePath):
        return return_error(f"Domain {domainName} already exists", 409)

    with open(filePath, "w") as f:
        domain = {"domainName": domainName, "records": {}}
        json.dump(domain, f, indent=4)

    domain = {"domainName": domainName,
              "resource": f"/api/domains/{domainName}", "uri": f"{domainName}.{tld}", "records": f"/api/domains/{domainName}/records"}

    return return_json(domain)
