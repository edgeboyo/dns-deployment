import argparse
from ast import parse


def prepParser():
    parser = argparse.ArgumentParser(
        description='Start a DNS implemented in Python. Usually DNSs use UDP on port 53.')
    parser.add_argument('--dns-port', default=53, type=int,
                        help='The port to listen on for the DNS server.')
    parser.add_argument('--http_port', default=80, type=int,
                        help='The port to listen on for the HTTP API and GUI.')
    parser.add_argument('--tld', default="tld", type=str,
                        help="The top level domain of this DNS deployment (default \".tld\")")
    parser.add_argument('--data-folder', default="./data", type=str,
                        help="Location of DNS files being stored (default \"./data\")")
    parser.add_argument('--ssga-path', default="ssga", type=str,
                        help="Location of the semantic similarity analyzer [SSGA] (default \"ssga\" for Linux and \"ssga.exe\" for Windows)")
    parser.add_argument('--tcp', action='store_true',
                        help='Prepare a TCP DNS server')
    parser.add_argument('--udp', action='store_true',
                        help='Prepare a UDP DNS server')
    parser.add_argument('--dry-run', action="store_true",
                        help="Initialize the program, check arguments and exit immediately")

    return parser
