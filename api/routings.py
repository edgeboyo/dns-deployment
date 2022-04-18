from flask import Flask, request

from objects.domain import createNewDomain, fetchAllDomainNames

from api.returns import return_json, return_error

tld = "tld"  # will be imported from config later

app = Flask(__name__)


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
    for domainName in fetchAllDomainNames():
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

    try:
        createNewDomain(domainName)
    except Exception as e:
        return return_error(str(e), 409)

    domain = {"domainName": domainName,
              "resource": f"/api/domains/{domainName}", "uri": f"{domainName}.{tld}", "records": f"/api/domains/{domainName}/records"}

    return return_json(domain)


@app.route("/api/domains/{domainName}", methods=["GET"])
def api_domain_details(domainName):
    pass
