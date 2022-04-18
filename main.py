#!/usr/bin/env python
"""
LICENSE http://www.apache.org/licenses/LICENSE-2.0
"""

import http
import sys
import time
import threading

import threading
from api.api import api_startup

from ArgumentParser import prepParser
from dns.dns import createDNSServer


def error_out(message, code=2):
    print(message)
    exit(code)


def startup_checklist():
    parser = prepParser()

    args = parser.parse_args()

    # Select DNS server type (TCP/UDP)
    dns_type = None

    if args.tcp and args.udp:
        error_out("Currently cannot run both server types at the same time")
    elif args.tcp:
        dns_type = "TCP"
    elif args.udp:
        dns_type = "UDP"
    else:
        error_out("Either --tcp or --udp are required")

    # Select DNS server port and check if valid
    dns_port = args.dns_port

    if dns_port <= 0:
        error_out("[DNS] Port number must be less higher than 0")

    # Select HTTP server port and check if valid
    http_port = args.http_port

    if http_port <= 0:
        error_out("[HTTP] Port number must be less higher than 0")

    if http_port == dns_port:
        error_out(
            "To ensure interoperability the port number need to differ even if on separate protocols")

    if args.dry_run:
        print("This configuration appears valid. Ending program due to dry run argument")
        exit()

    return (dns_type, dns_port, http_port)


def server_startup(dns_type, dns_port, http_port):

    print("Starting API...")

    httpServer = threading.Thread(target=api_startup, args=(http_port, ))
    httpServer.daemon = True
    httpServer.start()

    print("Starting nameserver...")

    dnsServer = createDNSServer(dns_type, dns_port)

    try:
        while 1:
            time.sleep(1)
            sys.stderr.flush()
            sys.stdout.flush()

    except KeyboardInterrupt:
        pass
    finally:
        dnsServer.shutdown()


if __name__ == '__main__':
    (dns_type, dns_port, http_port) = startup_checklist()
    server_startup(dns_type, dns_port, http_port)
