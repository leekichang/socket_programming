#client.py

import threading
import time
from socket import *
import pickle
import numpy as np
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description='Socket Programming')
    parser.add_argument('--ip', default='192.168.0.4')
    parser.add_argument('--p', default=9784)
    args = parser.parse_args()
    return args

class Client:
    def __init__(self, SERVER_ADDRESS):
        self.socket = socket(AF_INET, SOCK_STREAM)
        self.socket.connect(SERVER_ADDRESS)
        print("Client Connected!")
        self.LOCK = threading.Lock()

    def send(self):
        while True:
            try:
                data = int(input('>>>'))
                self.socket.send(pickle.dumps(data))
                print('전송완료')
                if data == 0:
                    print("연결 종료")
                    break
            except:
                break

    def recv(self):
        while True:
            recv_data = b''
            while True:
                chunk = self.socket.recv(16384)
                recv_data += chunk
                if len(chunk) < 16384:
                    break
            if not recv_data:
                print('no receive data')
                break
            print('받은 데이터:', pickle.loads(recv_data))

    def create_thread(self):
        self.sender   = threading.Thread(target=self.send)
        self.sender.daemon = True
        self.receiver = threading.Thread(target=self.recv)
        self.sender.daemon = True
    
    def run(self):
        self.create_thread()
        self.sender.start()
        self.receiver.start()
        self.sender.join()
        self.receiver.join()


if __name__ == '__main__':
    args = parse_args()
    SERVER_ADDRESS = (args.ip, args.p)
    client = Client(SERVER_ADDRESS)
    client.run()