# Socket for client
# Secured connection will be implemented at a later stage

import socket
from modules.Parser import Reader
from modules.Predict import run_predict_main

class ProcessData():
    def __init__(self, filename, format='csv'):
        self.filename = filename
        self.format = format
    
    def parse(self):
        self.reader = Reader(filename, 1)
        self.df = self.reader.read()
        return self.df
    
    def analyse(self):
        self.analysis = run_predict_main(self.df)
        return self.analysis
'''
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
    '''
    