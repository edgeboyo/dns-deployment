import socketserver
import datetime
import traceback
import struct
import sys

from .operators import dns_response

# These handleres make extensive use of an Open Source gist by pklaus on GitHub - https://gist.github.com/pklaus/b5a7876d4d2cf7271873


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


def createTCPServer(dns_port):
    return socketserver.ThreadingTCPServer(
        ('', dns_port), TCPRequestHandler)


def createUDPServer(dns_port):
    return socketserver.ThreadingUDPServer(
        ('', dns_port), UDPRequestHandler)
