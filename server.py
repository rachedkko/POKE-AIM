import socket
from _thread import*
import pickle
from game import*
import struct
import random
import time
g=["M",{},[int(w/2),int(h/2)],0,False,False,"0"]
#
x=(str.encode(str(g)))
data = eval(x)


def changepos(g):
    if g[0] == "P":
        g[2][0] = random.randrange(0 + 71, w - 71)
        g[2][1] = random.randrange(0, h - 62)
    else:
        g[2][0] = random.randrange(0 + 35, w - 35)
        g[2][1] = random.randrange(0, h - 31)


def changeball(g):
    g[0] = random.choice("MPPPPPPPPPP")


def reset(g):
    g[0] = "P"

    g[2] = [w / 2, h / 2]
    g[3] = 0

    g[4] = False
    g[5] = False

clientnb=0
server="192.168.1.44"
port=50
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)


try:

    s.bind((server,port))
except socket.error as e:
    print(e)

s.listen()
print("J'attend une connexion, Dresseur de Pokémon")
def thread(conn,p):
    global clientnb
    global g
    print(clientnb)
    g[1][p]=[0,0]

    conn.send(str.encode(str(p)))
    r=False

    reply=""
    while True:




        if g[3] == clientnb and clientnb > 1:
            print("jzdoihzeiod")
            plus = g[5]
            g = g[:4]
            g.append(True)
            g.append(plus)
        else:
            g[4]=False
        try:

            data=conn.recv(400).decode()

            if data=="ready":
                r=True
                g[3]+=1
                print("ozezezh")
            elif data=="clik":
                    print("x")
                    print(g[2])
                    changepos(g)
                    changeball(g)
                    print(g[2])
            elif data=="reset":
                reset(g)
                r=False
            elif data=="win":
                g[5]=True
            elif data=="get":
                reply = str.encode(str(g))


                if len(reply)>60:
                    while 60 - len(reply) != 0:
                        g[6]="0"
                        reply = str.encode(str(g))
                        print(len(reply))
                elif len(reply)<60:
                    while 60-len(reply)!=0:
                        g[6]+="0"
                        reply= str.encode(str(g))
                conn.sendall(reply)

            elif data!="get" and not "g" in data:

                co=eval(data)
                g[1][p]=co

            if not data:
                print("oh")
                if r:
                    g[3]-=1
                clientnb-=1
                del g[1][p]
                break






        except socket.error:
            print("ohh")
            if r:
                g[3] -= 1
            clientnb -= 1
            reset(g)
            break
    conn.close()
while True:
    conn,addr=s.accept()
    print(addr)
    p = clientnb
    start_new_thread(thread,(conn,p))

    clientnb+=1
