import socket
import os
import shutil
from threading import Thread
from socketserver import ThreadingMixIn
# Multithreaded Python server : TCP Server Socket Thread Pool
class ClientThread(Thread):
    def __init__(self,ip,port):
        Thread.__init__(self)
        self.ip = ip
        self.port = port
        print("New server socket thread started for " + ip + ":" + str(port))

    def removeArchive(self,nameAr):
        try:
            os.remove(nameAr)
            return True
        except OSError as e:
            print("Error: %s - %s." % (e.filename, e.strerror))
            return False

    def removeFile(self, nameFile):
        try:
            shutil.rmtree(nameFile)
            return True
        except OSError as e:
            print("Error: %s - %s." % (e.filename, e.strerror))

    def list(self, address):
        try:
            data = os.listdir(address)
            return data
        except OSError as e:
            print("Error: %s - %s." % (e.filename, e.strerror))
            return False
    def basePath(self):
        return os.getcwd()
    def path(self, basePath, userPath):
        path = os.path.join(basePath, userPath)
        path = os.path.abspath(path)
        return path
    def newFile(self,name):
        try:
            os.mkdir(name)
            return True
        except OSError as e:
            return e.filename, e.strerror
    def run(self):
        while True:
            data = conn.recv(BUFFER_SIZE)
            arrData = data.decode(encoding="utf-8").split("$")
            if len(arrData) >= 2:
                recibed = arrData[0]
                nameOfFile = arrData[1]
                print("Server received menssage: "+recibed)
                if recibed == "SD":
                    self.dataToRecibe(nameOfFile)
                elif recibed.lower() == "rma":
                    print(nameOfFile)
                    nameAr = nameOfFile  # guarda el nombre del archivo
                    stop = self.removeArchive(nameAr)
                    if stop:
                        conn.sendall(("success in the delete").encode())
                    else:
                        msg1 = "error in the delete, try again"
                        conn.sendall(msg1.encode())
                elif recibed.lower() == "rmf":
                        stop = self.removeFile(nameOfFile)
                        if stop:
                            conn.sendall(("success in the delete").encode())
                        else:
                            msg1 = "error in the delete, try again"
                            conn.sendall((msg1).encode())
                elif recibed.lower() == "list":
                    basePath = nameOfFile
                    userPath = arrData[2]
                    path = self.path(basePath, userPath)
                    conn.sendall(str(path).encode())
                    data1 = self.list(path)
                    if data1 != False:
                        conn.sendall((str(data1).encode()))
                    else:
                        msg1 = "error in the path, try again"
                        conn.sendall((msg1).encode())
                elif recibed.lower() == "basepath":
                    address = self.basePath()
                    conn.sendall((str(address).encode()))
                elif recibed.lower() == "nf":
                    file = self.newFile(nameOfFile)
                    if file == True:
                        conn.sendall(("Success in file creation").encode())
                    else:
                        conn.sendall(("error: " + file[0] + " " + file[1]).encode())
    def dataToRecibe(self,file):
        recived_f = file
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


# Multithreaded Python server : TCP Server Socket Program Stub
TCP_IP = '0.0.0.0'
TCP_PORT = 2004
BUFFER_SIZE = 80096  # Usually 1024, but we need quick response

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
