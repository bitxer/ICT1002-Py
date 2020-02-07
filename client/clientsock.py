# Socket for client
# Secured connection will be implemented at a later stage

import socket

class ClientSocket():
    def __init__(self, hostname='localhost', port=8443):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((hostname, port))

    def send(self, data, buf=2048):
        for i in range(0, len(data), buf):
            self.sock.sendall(data[i: i + buf])
        print(data)
        self.sock.sendall(b'bitxer')
    
    def recv(self, buf=2048, timeout=10):
        return self.sock.recv(buf)
    