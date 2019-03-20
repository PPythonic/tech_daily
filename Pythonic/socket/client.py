import socket
import struct
import json
import time


class Client(object):
    addr = ('127.0.0.1', 8080)

    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect(self.addr)
        print("connect to server")

    def get_request(self):
        while True:
            request = input(">>>").strip()
            if not request:
                continue
            
            return request

    def recv(self):
        # 拆包接收
        struct_bytes = self.socket.recv(4)
        header_len = struct.unpack('i', struct_bytes)[0]
        header_bytes = self.socket.recv(header_len)
        header = json.loads(header_bytes.decode('utf-8'))
        data_len = header['data_len']

        gap_abs = data_len % 1024
        count = data_len // 1024
        recv_data = b''

        for i in range(count):
            data = self.socket.recv(1024, socket.MSG_WAITALL)
            recv_data += data
        recv_data += self.socket.recv(gap_abs)

        print('recv data len is: ', len(recv_data))
        return recv_data

    def run(self):
        while True:  # 消息循环
            request = self.get_request()
            self.socket.send(request.encode('utf-8'))
            response = self.recv()
            print(response.decode('utf-8'))
    

if __name__ == "__main__":
    client = Client()
    client.run()
