import os
import json
from flask import Flask

tld = "tld"  # will be imported from config later

app = Flask(__name__)


def return_json(object, code=200):
    response = app.response_class(
        response=json.dumps(object),
        status=code,
        mimetype="application/json"
    )
    return response


@app.route("/")
def gui_root():
    return "<p>This will be the GUI root later</p>"


@app.route("/api/")
def api_root():
    data = {"documentation": "/api/docs",
            "topLevelDomain": f".{tld}", "domains": "/api/domains"}
    return return_json(data)


@app.route("/api/domains/")
def api_domains():
    domains = []
    for file in os.listdir('./data'):
        if not os.fsdecode(file).endswith('.json'):
            continue

        filePath = f"./data/{file}"

        with open(filePath) as f:
            domainInfo = json.load(f)
            domainName = domainInfo['name']

        domain = {"domainName": domainName,
                  "resource": f"/api/domains/{domainName}", "uri": f"{domainName}.{tld}", "records": f"/api/domains/{domainName}/records"}

        domains.append(domain)

    return return_json(domains)
