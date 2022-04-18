
def createDNSServer(dns_type, dns_port):
    if dns_type == 'TCP':
        return socketserver.ThreadingTCPServer(
            ('', dns_port), TCPRequestHandler)
    elif dns_type == 'UDP':
        return socketserver.ThreadingUDPServer(
            ('', dns_port), UDPRequestHandler)
