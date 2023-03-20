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
        self.socket.sendall(pickle.dumps(data))
        print('전송완료')
        if data == 0:
            print("연결 종료")

    # def recv(self):
    #     # First, receive the length of the data
    #     data_len_bytes = self.socket.recv(4)
    #     data_len = int.from_bytes(data_len_bytes, byteorder='big')

    #     # Then, receive the data itself in chunks
    #     recv_data = []
    #     while data_len > 0:
    #         chunk = self.socket.recv(min(data_len, 4096))
    #         recv_data.append(chunk)
    #         if len(chunk) < 4096:
    #             break
    #         data_len -= len(chunk)
    #     if not recv_data:
    #         print('no receive data')
    #     print('받은 데이터:', pickle.loads(b''.join(recv_data)))

    def recv(self):
        data_total_len     = int(self.socket.recv(1024))
        left_recv_len      = data_total_len
        buffer_size        = data_total_len
        time.sleep(1)

        recv_data = []
        while True:
            chunk = self.socket.recv(data_total_len)
            recv_data.append(chunk)
            left_recv_len -= len(chunk)
            if left_recv_len <= 0:
                break
        print(f'받은 데이터:{pickle.loads(b"".join(recv_data))}\n\n{total_len}')

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


