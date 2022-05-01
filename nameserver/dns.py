
from nameserver.handlers import createTCPServer, createUDPServer
import threading


class ServerHolder():
    def __init__(self, servers):
        self.servers = servers

    def run(self):
        for server in self.servers:
            thread = threading.Thread(target=server.serve_forever)
            thread.daemon = True  # exit the server thread when the main thread terminates
            thread.start()
            print("%s server loop running in thread: %s" %
                  (server.RequestHandlerClass.__name__[:3], thread.name))

    def shutdown(self):
        for server in self.servers:
            server.shutdown()


def createDNSServer(dns_type, dns_port):
    server = []
    if 'TCP' in dns_type:
        server += [createTCPServer(dns_port)]

    if 'UDP' in dns_type:
        server += [createUDPServer(dns_port)]

    server = ServerHolder(server)

    server.run()

    return server
