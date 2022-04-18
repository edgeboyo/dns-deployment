#!/usr/bin/env python
"""
LICENSE http://www.apache.org/licenses/LICENSE-2.0
"""

from ast import arg
import datetime
import sys
import time
import threading
import traceback
import socketserver
import struct

import threading
from api.api import api_startup

from ArgumentParser import prepParser
try:
    from dnslib import *
except ImportError:
    print("Missing dependency dnslib: <https://pypi.python.org/pypi/dnslib>. Please install it with `pip`.")
    sys.exit(2)


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


def dns_response(data):
    request = DNSRecord.parse(data)

    print(request)

    reply = DNSRecord(DNSHeader(id=request.header.id,
                      qr=1, aa=1, ra=1), q=request.q)

    qname = request.q.qname
    qn = str(qname)
    qtype = request.q.qtype
    qt = QTYPE[qtype]

    if qn == D or qn.endswith('.' + D):

        for name, rrs in records.items():
            if name == qn:
                for rdata in rrs:
                    rqt = rdata.__class__.__name__
                    if qt in ['*', rqt]:
                        reply.add_answer(RR(rname=qname, rtype=getattr(
                            QTYPE, rqt), rclass=1, ttl=TTL, rdata=rdata))

        for rdata in ns_records:
            reply.add_ar(RR(rname=D, rtype=QTYPE.NS,
                         rclass=1, ttl=TTL, rdata=rdata))

        reply.add_auth(RR(rname=D, rtype=QTYPE.SOA,
                       rclass=1, ttl=TTL, rdata=soa_record))

    print("---- Reply:\n", reply)

    return reply.pack()


class BaseRequestHandler(socketserver.BaseRequestHandler):

    def get_data(self):
        raise NotImplementedError

    def send_data(self, data):
        raise NotImplementedError

    def handle(self):
        now = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')
        print("\n\n%s request %s (%s %s):" % (self.__class__.__name__[:3], now, self.client_address[0],
                                              self.client_address[1]))
        try:
            data = self.get_data()
            print(len(data), data)  # repr(data).replace('\\x', '')[1:-1]
            self.send_data(dns_response(data))
        except Exception:
            traceback.print_exc(file=sys.stderr)


class TCPRequestHandler(BaseRequestHandler):

    def get_data(self):
        data = self.request.recv(8192).strip()
        sz = struct.unpack('>H', data[:2])[0]
        if sz < len(data) - 2:
            raise Exception("Wrong size of TCP packet")
        elif sz > len(data) - 2:
            raise Exception("Too big TCP packet")
        return data[2:]

    def send_data(self, data):
        sz = struct.pack('>H', len(data))
        return self.request.sendall(sz + data)


class UDPRequestHandler(BaseRequestHandler):

    def get_data(self):
        return self.request[0].strip()

    def send_data(self, data):
        return self.request[1].sendto(data, self.client_address)


def startup_checklist():
    parser = prepParser()

    args = parser.parse_args()

    return None


def server_startup(dns_type, dns_port, http_port, dry_run):

    print("Starting API...")

    httpServer = threading.Thread(target=api_startup, args=(http_port, ))
    httpServer.daemon = True
    httpServer.start()

    print("Starting API...")

    httpServer = threading.Thread(target=api_startup, args=(args.aport , ))
    httpServer.daemon = True
    httpServer.start()

    print("Starting nameserver...")

    dnsServer = None

    for s in servers:
        # that thread will start one more thread for each request
        thread = threading.Thread(target=s.serve_forever)
        thread.daemon = True  # exit the server thread when the main thread terminates
        thread.start()
        print("%s server loop running in thread: %s" %
              (s.RequestHandlerClass.__name__[:3], thread.name))

    def shutdown():
        for s in servers:
            s.shutdown()

    if dry_run:
        shutdown()
        return

    def shutdown():
        for s in servers:
            s.shutdown()

    if args.dry_run:
        shutdown()
        return

    try:
        while 1:
            time.sleep(1)
            sys.stderr.flush()
            sys.stdout.flush()

    except KeyboardInterrupt:
        pass
    finally:
        shutdown()

if __name__ == '__main__':
    (dns_type, dns_port, http_port, dry_run) = startup_checklist()
    server_startup(dns_type, dns_port, http_port, dry_run)
