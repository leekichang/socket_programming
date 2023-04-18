#client.py

import threading
import time
from socket import *
import pickle
import numpy as np
import argparse

class Client:
    def __init__(self, SERVER_ADDRESS):
        self.socket = socket(AF_INET, SOCK_STREAM)
        self.socket.connect(SERVER_ADDRESS)
        self.connected = True
        print("Client Connected!")

    def send(self):
        data = int(input('>>>'))
        self.socket.sendall(pickle.dumps(data))
        print('전송완료')
        if data == 0:
            print("연결 종료")
            self.connected = False
            self.socket.close()

    def recv(self):
        data_total_len     = int(self.socket.recv(1024))
        left_recv_len      = data_total_len
        buffer_size        = data_total_len
        time.sleep(1)

        recv_data = []
        while True:
            chunk = self.socket.recv(buffer_size)
            recv_data.append(chunk)
            left_recv_len -= len(chunk)
            if left_recv_len <= 0:
                break
        if not left_recv_len == 0:
            print("Packet Loss!")
        else:
            print(f'받은 데이터:{pickle.loads(b"".join(recv_data))}\n\n{data_total_len}')
    
    def run(self):
        while True:
            self.send()
            if not self.check_connection():break
            self.recv()
            if not self.check_connection():break

    def check_connection(self):
        return self.connected

if __name__ == '__main__':
    args = parse_args()
    SERVER_ADDRESS = (args.ip, args.p)
    client = Client(SERVER_ADDRESS)
    client.run()


