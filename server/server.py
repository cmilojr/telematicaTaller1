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
    def sendData(self, nameOfFile):
        print("--------------Sending...--------------")
        filename = nameOfFile
        f = open(filename, 'rb')
        while True:
            l = f.read(BUFFER_SIZE)
            print(f"value of L is: {l}")
            while (l):
                conn.send(l)
                print('Sent ',repr(l))
                l = f.read(BUFFER_SIZE)
            if not l:
                f.close()
                #tcpClientB.close()
                break
        print("-----------Finished sending data-----------")
    def move(self, name, destination):
        try:
            shutil.move(name, destination)
            return True
        except shutil.Error as e:
            return e

    def run(self):
        while True:
            data = conn.recv(BUFFER_SIZE)
            arrData = data.decode(encoding="utf-8").split("<separator>")
            if len(arrData) >= 2:
                recibed = arrData[0]
                nameOfFile = arrData[1]
                print("Server received menssage: "+recibed)
                if recibed.lower() == "sd":
                    self.dataToRecibe(nameOfFile)
                    destinacion = arrData[2]
                    move = self.move(nameOfFile, destinacion)
                    if move == True:
                        conn.sendall(("success in the upload").encode())
                    else:
                        conn.sendall(move.__str__().encode())
                elif recibed.lower() == 'dd':
                    self.sendData(arrData[1])
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
                    data1 = self.list(path)
                    if data1 != False:
                        conn.sendall((str(path) + "@" + str(data1)).encode())
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
                else:
                    conn.sendall(("error code").encode())
                    print("error code from client")

    def dataToRecibe(self,file):
        recived_f = file
        with open(recived_f, 'wb') as f:
            print('file opened')
            while True:
                print('receiving data...')
                data = conn.recv(BUFFER_SIZE)
                print(f"data recived = {data}")
                f.write(data)
                #if not data:
                print('finished receiving data.')
                f.close()
                print('file close()')
                break
                #f.write(data)
        print('Successfully get the file')   


SERVER = '0.0.0.0'
PORT = 2004
ADDRESS = (SERVER,PORT)
BUFFER_SIZE = 1024 

tcpServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpServer.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
tcpServer.bind(ADDRESS)

try:
    tcpServer.bind(ADDRESS)
    print(f"Listening as {SERVER} : {PORT}")
except socket.error as msg:
    print("Socket Binding error" + str(msg) + "\n" + "Retrying...")

while True:
    tcpServer.listen(4)
    print("Multithreaded Python server : Waiting for connections from TCP clients...")
    (conn, (ip,port)) = tcpServer.accept()
    print(f"{ip} is connected in the port {port}.")

    newthread = ClientThread(ip,port)
    newthread.daemon = True
    newthread.start()
