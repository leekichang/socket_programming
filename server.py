#server.py
import threading
import time
from socket import *
import pickle
import numpy as np
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description='Socket Programming')
    parser.add_argument('--p', default=9784, type=int)
    args = parser.parse_args()
    return args

class Server:
    def __init__(self, SERVER_ADDRESS):
        self.address  = SERVER_ADDRESS
        self.socket   = socket(AF_INET, SOCK_STREAM)
        self.socket.bind(self.address)
        self.socket.listen(1)
        print("server is ready")
        self.client_socket, self.client_addr = self.socket.accept()
        print(f"server connected by {self.client_addr}")
        self.request = None
        self.connected = True

    def send(self):
        if self.request != None and self.request != 0:
            data = np.random.rand(self.request)
            self.client_socket.send(pickle.dumps(data))
            print("DATA SENT")
            self.request = None
        
    
    def recv(self):
        recv_data = []
        while True:
            chunk = self.client_socket.recv(1024)
            recv_data.append(chunk)
            if len(chunk) < 1024:
                break
        # recv_data = self.client_socket.recv(4096)
        data = pickle.loads(b''.join(recv_data))
        if data == 0:
            self.client_socket.close()
            self.connected = False
            print("DISCONNECTED")
            self.connect()
        
        print(f"RECEIVCED DATA: {data}")
        self.request = data
        
    def connect(self):
        print("WAITING FOR NEW CONNECTION")
        self.socket.listen(1)
        self.client_socket, self.client_addr = self.socket.accept()
        print(f"server connected by {self.client_addr}")
        self.is_connected = True
    
    def run(self):
        while True:
            self.recv()
            self.send()

if __name__ == '__main__':
    args = parse_args()
    SERVER_ADDRESS = ('0.0.0.0', args.p)
    server = Server(SERVER_ADDRESS)
    server.run()