import argparse

def prepParser():
    parser = argparse.ArgumentParser(description='Start a DNS implemented in Python. Usually DNSs use UDP on port 53.')
    parser.add_argument('--dport', default=53, type=int, help='The port to listen on for the DNS server.')
    parser.add_argument('--aport', default=80, type=int, help='The port to listen on for the HTTP API and GUI.')
    parser.add_argument('--tcp', action='store_true', help='Listen to TCP connections.')
    parser.add_argument('--udp', action='store_true', help='Listen to UDP datagrams.')

    return parser

