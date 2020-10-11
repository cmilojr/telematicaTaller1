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
        print("New server socket thread started for " + ip + ":" + str(port))

    def run(self):
        while True:
            data = conn.recv(BUFFER_SIZE)
            arrData = data.decode(encoding="utf-8").split()
            if len(arrData) >= 2:
                recibed = arrData[0]
                nameOfFile = arrData[1]
                print("Server received menssage: "+recibed)
                if recibed == "SD":
                        recived_f = nameOfFile
                        with open(recived_f, 'wb') as f:
                            print('file opened')
                            while True:
                                print('receiving data...')
                                data = conn.recv(BUFFER_SIZE)
                                print(f"data = {data}")
                                if not data:
                                    print('finished receiving data.')
                                    f.close()
                                    print('file close()')
                                    break
                                # write data to a file
                                f.write(data)
                        print('Successfully get the file')   

    def dataToRecibe(self,file):
        recived_f = file
        with open(recived_f, 'wb') as f:
            print('file opened')
            while True:
                print('receiving data...')
                data = tcpServer.recv(BUFFER_SIZE)
                print('data=%s', (data))
                if not data:
                    f.close()
                    print('file close()')
                    break
                f.write(data)


# Multithreaded Python server : TCP Server Socket Program Stub
TCP_IP = '0.0.0.0'
TCP_PORT = 2004
BUFFER_SIZE = 4096  # Usually 1024, but we need quick response

tcpServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpServer.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
tcpServer.bind((TCP_IP, TCP_PORT))
threads = []

try:
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
