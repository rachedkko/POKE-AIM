import socket
from _thread import*
import pickle
import sys
from game import*
import struct
import time
g=Game()
clientnb=0
server="192.168.1.43"
port=50
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
chrono=0


def sendData( server_sock, object ):
    result = True
    data = pickle.dumps( object )
    data_size = struct.pack( '!I', len( data ) )  # good for 2^32 bytes

    try:

        server_sock.sendall(data_size)   # send the size of the pickled obj
        server_sock.sendall(data)        # send the obj
    except socket.error as e:
        print(e)
        sys.stderr.write( "Error sending data to server\n" )
        result = False
    return result

try:

    s.bind((server,port))
except socket.error as e:
    print(e)

s.listen()
print("J'attend une connexion, Dresseur de Pokémon")
def thread(conn,p,s):
    global clientnb
    global g
    global chrono
    print(clientnb)
    g.pos[p]=(0,0)

    conn.send(str.encode(str(p)))
    r=False

    reply=""
    while True:

        sendData(conn, g)
        print(time.time()-chrono)

        if g.ready == clientnb and clientnb > 1:
            g.start=True
        else:
            g.start=False
        try:

            data=conn.recv(4096).decode()

            if data=="ready":
                r=True
                g.ready+=1
            elif data=="clik":
                    print("x")
                    print(g.ball)
                    g.changepos()
                    g.changeball()
                    print(g.ball)
            elif data=="reset":
                g.reset()
                r=False
            elif data=="win":
                g.end=True


            elif data!="get" and data!=None:

                co=eval(data)
                g.pos[p]=co
                chrono = time.time()
            elif not data:
                print("oh")
                if r:
                    g.ready-=1
                clientnb-=1
                del g.pos[p]
                break



        except :
            print("ohh")
            if r:
                g.ready -= 1
            clientnb -= 1
            g.reset()
            break
    conn.close()
while True:
    conn,addr=s.accept()
    print(addr)
    p = clientnb
    start_new_thread(thread,(conn,p,s))

    clientnb+=1