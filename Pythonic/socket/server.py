import socket
import subprocess
import sys
import json
import struct
from concurrent.futures import ThreadPoolExecutor

def init_socket():
    addr = ('127.0.0.1', 8080)
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(addr)
    server.listen(5)
    print('Starting listen')
    return server

def handle(request):
    command = request.decode('utf-8')
    obj = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    result = obj.stdout.read() + obj.stderr.read()
    # 如果是win要转换编码
    if sys.platform == 'win32':
        result = result.decode('gbk').encode('utf-8')
    return result

def build_header(data_len):
    dic = {
        'cmd_type': 'shell',
        'data_len': data_len,
    }
    return json.dumps(dic).encode('utf-8')

def send(conn, response):
    data_len = len(response)
    header = build_header(data_len)
    header_len = len(header)
    struct_bytes = struct.pack('i', header_len)

    # 粘包发送
    conn.send(struct_bytes)
    conn.send(header)
    conn.send(response)


def task(conn):
    try:
        while True:  # 消息循环
            request = conn.recv(1024)
            if not request:
                # 链接失效
                raise ConnectionResetError

            response = handle(request)
            send(conn, response)
            
    except ConnectionResetError:
        msg = f'链接-{conn.getpeername()}失效'
        conn.close()
        return msg

def show_res(future):
    result = future.result()
    print(result)

if __name__ == "__main__":
    max_thread = 5
    futures = []
    server = init_socket()
    with ThreadPoolExecutor(max_thread) as pool:
        while True:  # 连接循环
            conn, addr = server.accept()
            print(f'一个客户端上线{addr}')

            future = pool.submit(task, conn)
            future.add_done_callback(show_res)
            futures.append(future)