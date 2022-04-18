import argparse


def prepParser():
    parser = argparse.ArgumentParser(
        description='Start a DNS implemented in Python. Usually DNSs use UDP on port 53.')
    parser.add_argument('--dns-port', default=53, type=int,
                        help='The port to listen on for the DNS server.')
    parser.add_argument('--http_port', default=80, type=int,
                        help='The port to listen on for the HTTP API and GUI.')
    parser.add_argument('--tcp', action='store_true',
                        help='Listen to TCP connections.')
    parser.add_argument('--udp', action='store_true',
                        help='Listen to UDP datagrams.')
    parser.add_argument('--dry-run', action="store_true",
                        help="Initialize the program, check arguments and exit immediately")

    return parser
