import argparse


def prepParser():
    parser = argparse.ArgumentParser(
        description='Start a DNS implemented in Python. Usually DNSs use UDP on port 53.')
    parser.add_argument('-d', dest='docker', action="store_true",
                        help="Set this flag to use internal docker addresses (for docker deployment)")
    parser.add_argument('--dns-port', default=53, type=int,
                        help='The port to listen on for the DNS server.')
    parser.add_argument('--http-port', default=80, type=int,
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
    parser.add_argument('--fallback-dns', default="1.1.1.1", type=str,
                        help="Address to a DNS used as authority when the domain requested is not under this server")
    parser.add_argument('--no-metrics', action='store_true',
                        help="Allow for the deployment to not collect metrics")
    parser.add_argument('--influx-port', default=8086, type=int,
                        help="Set a custom port for influxDB")
    parser.add_argument('--influx-username', default="superuser", type=str,
                        help="Set a custom username for influxDB (default \"superuser\"")
    parser.add_argument('--influx-password', default="superuser_passwd", type=str,
                        help="Set a custom username for influxDB (default \"superuser_passwd\"")
    parser.add_argument('--metrics-consumers', default=5, type=int,
                        help="Set custom amount of metrics consumer threads (default 5)")

    return parser
