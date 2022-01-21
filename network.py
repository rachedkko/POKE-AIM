import socket
import pickle
import struct
class Network:
    def __init__(self):
        self.client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.server="192.168.1.44"
        self.port=50
        self.addr=(self.server,self.port)
        self.p=self.connect()

    def getP(self):
        return self.p
    def connect(self):
        try:
            self.client.connect(self.addr)
            return self.client.recv(150).decode()
        except:
            pass
    def sendd(self,data):
        try:
            self.client.send(str.encode(data))


        except socket.error as e:
            print(e)

    def send(self,data):
        try:
            self.client.send(str.encode(data))

            return self.client.recv(150).decode()
        except socket.error as e:
            print(e)
