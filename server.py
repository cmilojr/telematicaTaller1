import socket
import tqdm
import os
from threading import Thread
from socketserver import ThreadingMixIn

# Multithreaded Python server : TCP Server Socket Thread Pool
class ClientThread(Thread):
    def __init__(self,ip,port):
        Thread.__init__(self)
        self.ip = ip
        self.port = port
        print("[+] New server socket thread started for " + ip + ":" + str(port))

    def run(self):
        print("inicie")
        while True :
            data = conn.recv(BUFFER_SIZE)
            recibed = data.decode(encoding="utf-8")
            
            if recibed != "":
                print("Server received data: "+recibed)
            # MESSAGE = input("Multithreaded Python server : Enter Response from Server/Enter exit:")
            # if MESSAGE == 'exit':
            #     break
            # conn.send(MESSAGE.encode())  # echo

# Multithreaded Python server : TCP Server Socket Program Stub
TCP_IP = '0.0.0.0'
TCP_PORT = 2004
BUFFER_SIZE = 4096  # Usually 1024, but we need quick response
SEPARATOR = "<SEPARATOR>"

tcpServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpServer.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
tcpServer.bind((TCP_IP, TCP_PORT))
threads = []

try:
    threads = []
    tcpServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcpServer.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        tcpServer.bind((TCP_IP, TCP_PORT))
        print(f"Listening as {TCP_IP} : {TCP_PORT}")
    except socket.error as msg:
        print("Socket Binding error" + str(msg) + "\n" + "Retrying...")

    while True:
        tcpServer.listen(4)
        print("Multithreaded Python server : Waiting for connections from TCP clients...")
        (conn, (ip,port)) = tcpServer.accept()
        print(f"{ip} is connected in the port {port}.")

        newthread = ClientThread(ip,port)
        newthread.start()
        threads.append(newthread)

    for t in threads:
        t.join()

except socket.error as msg:
    print("Socket creation error: " + str(msg))
