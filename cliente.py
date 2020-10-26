# Python TCP Client B
import os
import socket
import threading
import shutil
host = socket.gethostname()
port = 2004
BUFFER_SIZE = 2000

MESSAGE = ""
tcpClientB = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
def work():
    try: 
        tcpClientB.connect((host, port))
        while True:#MESSAGE != 'exit':
            MESSAGE = input("Client: Enter code / Enter exit: ")
            if MESSAGE.lower() == "exit":
                break
            if MESSAGE.lower() == 'sd':
                try:
                    path = input("Enter name of path to save\n-> ")
                    nameOfFile = input("Enter name of file to upload with extension\n-> ")
                    try:
                        open(nameOfFile, 'rb')
                        tcpClientB.send((MESSAGE + "<separator>" + nameOfFile + "<separator>" + path).encode())
                        sendData(nameOfFile)
                        move = tcpClientB.recv(8000)
                        print(move.decode())
                    except OSError as a:
                        print(a.strerror)
                except:
                    print("Error sending data")
            #MESSAGE = input("Enter code / Enter exit: ")
            #tcpClientB.send(MESSAGE.encode())
            elif MESSAGE.lower() == 'dd': 
                try:
                    destination = input("Enter name of path to save\n-> ")
                    nameOfFile = input("Enter name of file to download with extension\n-> ")
                    tcpClientB.send((MESSAGE + "<separator>" + nameOfFile).encode())
                    a = tcpClientB.recv(8000).decode()
                    if a == "yes":
                        dataToRecibe(nameOfFile)
                        move = moveFile(nameOfFile, destination)
                        if move == "success":
                            print("success in save")
                        else:
                            print(move)
                    else:
                        print(a)
                except OSError as e:
                    print("error: " + e.strerror)
            elif MESSAGE.lower() == "rma":
                while True:
                    deleteName = input("Enter name of file to delete or enter  \" back \" to back\n-> ")
                    if deleteName.lower() == "back":
                        break
                    else:
                        tcpClientB.send((MESSAGE+"<separator>"+deleteName).encode())
                        msg = tcpClientB.recv(2000)
                        print(msg.decode())
            elif MESSAGE.lower() == "rmf":
                while True:
                    deleteName = input("Enter name of file to delete or enter  \" back \" to  back\n-> ")
                    if deleteName.lower() == "back":
                        break
                    else:
                        tcpClientB.send((MESSAGE+"<separator>"+deleteName).encode())
                        msg = tcpClientB.recv(2000)
                        print(msg.decode())
            elif MESSAGE.lower() == "list":
                tcpClientB.send(("basepath"+ "<separator>").encode())
                msg = tcpClientB.recv(80000)
                basePath = msg.decode()
                while True:
                    print("\n* current path = "+basePath)
                    pathName = input("* Enter name of the folder\n* enter \".\" to list the files of the current folder\n* use \"..\" to exit the folder\n* enter  \"back\" to exit list\n-> ")
                    if pathName.lower() == "back":
                        break
                    else:
                        tcpClientB.send((MESSAGE  + "<separator>" + basePath + "<separator>" + pathName).encode())
                        path = tcpClientB.recv(80000).decode().split("@")
                        if (path[0].lower() == "error in the path, try again"):
                            print(f"\n{path[0]}".upper())
                            basePath = basePath
                        else:
                            msg = path[1]
                            basePath = path[0]
                            print(f"\nfiles: {msg}\n")
            elif MESSAGE.lower() == "nf":
                while True:
                    deleteName = input("Enter name of folder to create  or enter  \" back \" to  back\n-> ")
                    if deleteName.lower() == "back":
                        break
                    else:
                        tcpClientB.send((MESSAGE+"<separator>"+deleteName).encode())
                        msg = tcpClientB.recv(2000)
                        print(msg.decode())
            else:
                print("invalid code in list")
        tcpClientB.close()
        print("connection end")
    except:
        print("Connection error to the server.")

def dataToRecibe(file):
    recived_f = file
    with open(recived_f, 'wb') as f:
        print('file opened')
        while True:
            print('receiving data...')
            data = tcpClientB.recv(BUFFER_SIZE)
            print(f"data recived = {data}")
            f.write(data)
            #if not data:
            print('finished receiving data.')
            f.close()
            print('file close()')
            break
            #f.write(data)
    print('Successfully get the file')


def moveFile( name, destination):
    if (os.path.isdir(destination)):
        try:
            shutil.move(name, destination)
            return True
        except OSError as e:
            return e
    else:
        os.remove(name)
        return "error: " + destination + " not exist"
def sendData(nameOfFile):
    print("--------------Sending...--------------")
    filename = nameOfFile

    f = open(filename, 'rb')
    while True:
        l = f.read(BUFFER_SIZE)
        print(f"value of L is: {l}")
        while (l):
            tcpClientB.send(l)
            print('Sent ',repr(l))
            l = f.read(BUFFER_SIZE)
        if not l:
            f.close()
            #tcpClientB.close()
            break

    print("-----------Finished sending data-----------")

n = threading.Thread(target=work)

n.start()