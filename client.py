#client.py

import threading
import time
from socket import *
import pickle
import numpy as np
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description='Socket Programming')
    parser.add_argument('--ip', default='192.168.0.4', type=str)
    parser.add_argument('--p', default=9784, type=int)
    args = parser.parse_args()
    return args

class Client:
    def __init__(self, SERVER_ADDRESS):
        self.socket = socket(AF_INET, SOCK_STREAM)
        self.socket.connect(SERVER_ADDRESS)
        print("Client Connected!")

    def send(self):
        data = int(input('>>>'))
        self.socket.send(pickle.dumps(data))
        print('전송완료')
        if data == 0:
            print("연결 종료")

    def recv(self):
        recv_data = []
        print("HI")
        while True:
            print("HEY~")
            chunk = self.socket.recv(4096)
            print("WASSUP")
            recv_data.append(chunk)
            if len(chunk) < 4096:
                break
        print("BYE")
        recv_bytes = b''.join(recv_data)

        if not recv_bytes:
            print('no receive data')
        print('받은 데이터:', pickle.loads(recv_bytes))

    # def recv(self):
    #     recv_data = []
    #     while True:
    #         chunk = self.socket.recv(100000)
    #         recv_data.append(chunk)
    #         if len(chunk) < 100000:
    #             break
    #     if not recv_data:
    #         print('no receive data')
    #     print('받은 데이터:', pickle.loads(b''.join(recv_data)))

    def create_thread(self):
        self.sender   = threading.Thread(target=self.send)
        self.sender.daemon = True
        self.receiver = threading.Thread(target=self.recv)
        self.sender.daemon = True
    
    def run(self):
        while True:
            self.send()
            self.recv()


if __name__ == '__main__':
    args = parse_args()
    SERVER_ADDRESS = (args.ip, args.p)
    client = Client(SERVER_ADDRESS)
    client.run()