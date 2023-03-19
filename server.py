#server.py
import threading
import time
from socket import *
import pickle
import numpy as np
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description='Socket Programming')
    parser.add_argument('--p', default=9784)
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
        self.LOCK = threading.Lock()
        self.request = None
        self.connected = True

    def send(self):
        while True:
            self.LOCK.acquire()
            if self.request != None and self.request != 0:
                # user_input = int(input('>>>'))
                data = np.random.rand(self.request)
                self.client_socket.send(pickle.dumps(data))
                print("DATA SENT")
                self.request = None
            self.LOCK.release()
    
    def recv(self):
        while True:
            try:
                recv_data = b''
                while True:
                    chunk = self.client_socket.recv(16384)
                    recv_data += chunk
                    if len(chunk) < 16384:
                        break
                # recv_data = self.client_socket.recv(4096)
                data = pickle.loads(recv_data)
                if data == 0:
                    self.LOCK.acquire()
                    self.client_socket.close()
                    self.connected = False
                    print("DISCONNECTED")
                    self.connect()
                    self.LOCK.release()
                self.LOCK.acquire()
                print(f"RECEIVCED DATA: {data}")
                self.request = data
                self.LOCK.release()
            except:
                pass
    
    def connect(self):
        print("WAITING FOR NEW CONNECTION")
        self.socket.listen(1)
        self.client_socket, self.client_addr = self.socket.accept()
        print(f"server connected by {self.client_addr}")
        self.is_connected = True

    def create_thread(self):
        self.sender   = threading.Thread(target=self.send)
        self.sender.daemon = True
        self.receiver = threading.Thread(target=self.recv)
        self.sender.daemon = True
    
    def run(self):
        self.create_thread()
        self.sender.start()
        self.receiver.start()
        while True:
            time.sleep(1)
            pass

if __name__ == '__main__':
    args = parse_args()
    SERVER_ADDRESS = ('0.0.0.0', args.p)
    server = Server(SERVER_ADDRESS)
    server.run()