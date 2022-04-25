
from dns.handlers import createTCPServer, createUDPServer
import threading


def createDNSServer(dns_type, dns_port):
    server = None
    if dns_type == 'TCP':
        server = createTCPServer(dns_port)
    elif dns_type == 'UDP':
        server = createUDPServer(dns_port)

    thread = threading.Thread(target=server.serve_forever)
    thread.daemon = True  # exit the server thread when the main thread terminates
    thread.start()
    print("%s server loop running in thread: %s" %
          (server.RequestHandlerClass.__name__[:3], thread.name))

    return server
