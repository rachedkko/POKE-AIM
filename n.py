import socket
import pickle
import struct
import sys
import time
class Network:
    def __init__(self):
        self.client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.server="192.168.1.43"
        self.port=50
        self.addr=(self.server,self.port)
        self.p=self.connect()

    def getP(self):
        return self.p
    def connect(self):
        try:
            self.client.connect(self.addr)
            return self.client.recv(4096).decode()
        except:
            pass

    def send(self,data):
        try:
            self.client.send(str.encode(data))
        except:
            pass

    def recvData(self):
        """ Try to receive a picked data-structure from the socket.
            Returns True and an unpicked object, or False and None   """

        result = False
        packet = None
        expected = -1

        # First we read a 4-byte pickle size, and following that is /N/ bytes
        # of pickled structure data.

        # Read the 4-byte packet size first
        buffer1 = bytes()
        while (len(buffer1) < 4):
            try:
                some_data = self.client.recv(4 - len(buffer1))
                if (some_data!=None):
                    buffer1+=(some_data)
                    if (len(buffer1) == 4):
                        expected = struct.unpack('!I', buffer1)
            except:
                # TODO: work out which sort of exceptions are OK
                break

        # If we received a buffer size, try to receive the buffer
        if (int(expected[0]) > 0):
            buffer2 = bytes()
            while (len(buffer2) < int(expected[0])):
                try:
                    some_data = self.client.recv(int(expected[0]) - len(buffer2))
                    if (some_data):
                        buffer2+=(some_data)
                        # Have we received the full data-set yet?
                        if (len(buffer2) == int(expected[0])):
                            packet = pickle.loads(buffer2)
                            result = True  # success
                except:

                    break

        return result, packet