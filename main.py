#!/usr/bin/env python
"""
LICENSE http://www.apache.org/licenses/LICENSE-2.0
"""

import os
import sys
import time
import threading

import threading
import traceback
from api.api import api_startup

from ArgumentParser import prepParser
from metrics.consumers import setUpInfluxDBClient, startMetricConsumers
from metrics.loggers import disableMetrics
from nameserver.dns import createDNSServer
from nameserver.operators import setResolver
from objects.domain import setTopLevelDomain
from objects.io import setDataFolder, setSSGAPath


def error_out(message, code=2):
    print(message)
    exit(code)


def startup_checklist():
    parser = prepParser()

    args = parser.parse_args()

    # Select DNS server type (TCP/UDP)

    dns_type = ""

    if args.tcp:
        dns_type += "TCP"
    if args.udp:
        dns_type += "UDP"

    if dns_type == "":
        error_out("Either --tcp or --udp or both are required")

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

    # Set the top level domain this DNS deployment manages

    setTopLevelDomain(args.tld)

    # Select data folder and set it internally

    setDataFolder(args.data_folder)

    # Select a fallback DNS servive for unknown TLDs

    setResolver(args.fallback_dns)

    # Select SSGA path, set it and check if valid

    try:
        setSSGAPath(args.ssga_path)
    except Exception as e:
        if os.name == 'nt':
            # This is an expected error, we can skip it
            if 'is not a valid file' not in str(e):
                traceback.print_exc()
            print()
            print("------------------------------------------------------------------")
            print("Error attempting to set SSGA path on Windows. Attempting with .exe")
            print("------------------------------------------------------------------")
            print()
            setSSGAPath(args.ssga_path + ".exe")
            print(".exe attempt passed. Continuing with script")
        else:
            print("Error detected on non-NT system")
            raise e

    # Disable metric collection if requested

    if args.no_metrics:
        disableMetrics()

    # Set up metric consumer threads

    startMetricConsumers(args.metrics_consumers)

    # Check if dry run was requested

    if args.dry_run:
        print("This configuration appears valid. Ending program due to dry run argument")
        exit()

    # Set up InfluxDB client (after dry run for CI safety)

    influx_url = '127.0.0.1' if not args.docker else 'influx-db'

    setUpInfluxDBClient(influx_url,
                        args.influx_port, args.influx_org, args.influx_token)

    return (dns_type, dns_port, http_port)


def server_startup(dns_type, dns_port, http_port):

    print("Starting API...")

    httpServer = threading.Thread(target=api_startup, args=(http_port, ))
    httpServer.daemon = True
    httpServer.start()

    time.sleep(.5)  # to allow for cleaner output

    print("Starting nameserver...")

    dnsServer = createDNSServer(dns_type, dns_port)

    try:
        while 1:
            time.sleep(1)
            sys.stderr.flush()
            sys.stdout.flush()

    except KeyboardInterrupt:
        exit()
    finally:
        dnsServer.shutdown()


if __name__ == '__main__':
    (dns_type, dns_port, http_port) = startup_checklist()
    server_startup(dns_type, dns_port, http_port)
