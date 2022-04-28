import re
from dnslib import *
import dns.resolver

from objects.domain import checkTLD, requestRecords

# All of this needs to go and has to fetch data from flat files in the data files


class DomainName(str):
    def __getattr__(self, item):
        return DomainName(item + '.' + self)


D = DomainName('example.com.')
IP = '127.0.0.1'
TTL = 60 * 5

soa_record = SOA(
    mname=D.ns1,  # primary name server
    rname=D.andrei,  # email of the domain administrator
    times=(
        201307231,  # serial number
        60 * 60 * 1,  # refresh
        60 * 60 * 3,  # retry
        60 * 60 * 24,  # expire
        60 * 60 * 1,  # minimum
    )
)
ns_records = [NS(D.ns1), NS(D.ns2)]
records = {
    D: [A(IP), AAAA((0,) * 16), MX(D.mail), soa_record] + ns_records,
    # MX and NS records must never point to a CNAME alias (RFC 2181 section 10.3)
    D.ns1: [A(IP)],
    D.ns2: [A(IP)],
    D.mail: [A(IP)],
    D.andrei: [CNAME(D)],
}

resolver = None


def setResolver(nameServer):
    global resolver

    resolver = dns.resolver.Resolver()
    resolver.nameservers = [nameServer]

    try:
        resolver.resolve("google.com")
    except:
        sys.exc_clear()
        raise Exception("Could not fetch Google.com. Fallback DNS invalid")


def interpret_local_records(records):
    pass


def prep_regex(domainName):
    regex = ""

    for c in domainName:
        if c == "*":
            c = "." + c

        if c == ".":
            c = "\\" + c

        regex += c

    return regex


def dns_response(data):
    request = DNSRecord.parse(data)

    print(request)

    reply = DNSRecord(DNSHeader(id=request.header.id,
                      qr=1, aa=1, ra=1), q=request.q)

    qname = request.q.qname
    qn = str(qname)
    qtype = request.q.qtype
    qt = QTYPE[qtype]

    if checkTLD(qn):
        records = requestRecords(qn)
        # records = interpretRecord(records)
        print(records)
    else:
        answer = resolver.resolve(qn, qt)
        print(answer.response)
        name = str(answer.qname)
        records = {name: []}
        for a in answer:
            # print(type(a))
            records[name].append((A(str(a)), None, answer.rrset.ttl))

    # All of this stuff might get thrown out
    for name, rss in records.items():
        regex = prep_regex(name)
        if re.match(regex, qn):
            for domainInfo in rss:
                (rdata, _, TTL) = domainInfo
                rqt = rdata.__class__.__name__
                if qt in ['*', rqt]:
                    reply.add_answer(RR(rname=qname, rtype=getattr(
                        QTYPE, rqt), rclass=1, ttl=TTL, rdata=rdata))

    # This code here is for NS and auth records. Since we don't use it now it should be omitted
    # Will be addressed later
    for rdata in ns_records:
        reply.add_ar(RR(rname=D, rtype=QTYPE.NS,
                        rclass=1, ttl=TTL, rdata=rdata))

    reply.add_auth(RR(rname=D, rtype=QTYPE.SOA,
                      rclass=1, ttl=TTL, rdata=soa_record))

    print("---- Reply:\n", reply)

    return reply.pack()