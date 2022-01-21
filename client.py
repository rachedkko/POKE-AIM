import pygame
import pickle
import sys
from network import Network
import time
import socket
pygame.font.init()

pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.mixer.init()
pygame.init()
run=True
timevar=False
pygame.mixer.music.load("music.mp3")
pygame.mixer.music.set_volume(0.1)
myscore=0
w=1280
h=720
screen= pygame.display.set_mode((w,h))
pygame.display.set_caption("Poké-Aim")
n=Network()
fond_color=(0,0,0)
color1 = (255, 0, 0)
click=pygame.mixer.Sound("click.ogg")




ball=pygame.transform.scale(pygame.image.load("ball.png").convert_alpha(),(71,62))
master=pygame.transform.scale(pygame.image.load("master.png").convert_alpha(),(35,31))
bigmaster=pygame.transform.scale(pygame.image.load("master.png").convert_alpha(),(71,62))
cursor=pygame.transform.scale(pygame.image.load("cursor.png").convert_alpha(),(48,48))
other_cursor=pygame.transform.scale(pygame.image.load("black_cursor.png").convert_alpha(),(48,48))
playing=False
loosing=False
winning=False
def find_key(v):
    for k, val in pos.items():
        if v == val:
            return k

clock=pygame.time.Clock()

ready=False
start=False
p=int(n.getP())
print(p)
pygame.mouse.set_visible(False)
while run:

    clock.tick(60)
    screen.fill(fond_color)
    try:
        euh=n.send("get")

        game =eval(euh)

    except socket.error as e:
        print(e)
        run=False
        print("Connexion perdue")
        break
    if game!=None:
        start=game[4]

        name=game[0]
        bol=game[2]
        pos=game[1]
        end=game[5]
        if game[3]==0:
            ready=False
    if not start:
        if not ready:
            color1=(255,0,0)
        font = pygame.font.Font("Pokemon Classic.ttf", 20)
        sc=font.render("= 1 pts", 1,(255,255,255) )
        sc2=font.render("= 3pts", 1,(255,255,255) )
        screen.blit(sc,(w/2,150))
        screen.blit(sc2, (w / 2, 215))
        screen.blit(ball,((w/2-80),140))
        screen.blit(bigmaster, ((w / 2 - 80), 200))

        text = font.render("Clique sur l'écran pour te mettre prêt !", 1,color1 )

        screen.blit(text, ((w - text.get_width()) / 2, (h - text.get_height()) / 2))
    elif start:

        screen.fill((255,244,10))
        if not playing:
            pygame.mixer.music.play()
            playing=True
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                while not ready:

                    color1 = (0,255, 0)

                    screen.blit(text, ((w - text.get_width()) / 2, (h - text.get_height()) / 2))

                    n.sendd("ready")
                    print("hzoizife")
                    click.play()
                    ready=True

                if start:
                    if name=="P":
                        if (bol[0]) <= (pygame.mouse.get_pos()[0] ) <= (bol[0] + 71):
                            if pygame.mouse.get_pos()[1]>= (bol[1]) and pygame.mouse.get_pos()[1] <= (bol[1] + 62):
                                click.play()
                                n.sendd("clik")
                                click.play()
                                myscore+=1
                    else:
                        if (bol[0]) <= (pygame.mouse.get_pos()[0] ) <= (bol[0] + 35):
                            if (pygame.mouse.get_pos()[1]) >= (bol[1]) and (pygame.mouse.get_pos()[1] )<= (bol[1] + 31):
                                click.play()
                                n.sendd("clik")
                                myscore+=3
    cord=[pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1]]
    try:
        n.client.send(str.encode(str(cord)))
    except :
        pass

    if start:
        if name=="P":
            screen.blit(ball, (int(bol[0]), int(bol[1])))
        else:
            screen.blit(master, (int(bol[0]), int(bol[1])))



        for e in pos.values():
            if find_key(e) != p:
                if find_key(e) != p:
                    screen.blit(other_cursor, (e[0]-24,e[1]-24))



    score = font.render(str(myscore), 1, (0,0,0))
    screen.blit(score, (5,0))
    if myscore >= 15:

        pygame.mixer.music.stop()

        screen.fill((0, 0, 0))
        wintext = font.render("T'as gagné sale bg !", 1, color1)
        screen.blit(wintext, ((w - wintext.get_width()) / 2, (h - wintext.get_height()) / 2))






        pygame.display.update()
        n.sendd("win")
        if not timevar:
            chrono=time.time()
            timevar=True
        if round(time.time()-chrono)>4:
            n.sendd("reset")

            color1 = (255, 0, 0)
            start = False
            ready = False
            playing = False
            myscore = 0
            timevar=False

            end = False
    elif end:

        pygame.mixer.music.stop()

        screen.fill((0, 0, 0))
        loosetext = font.render("T'as perdu t'es trop nul sérieux !", 1, (255,0,0))
        screen.blit(loosetext, ((w - loosetext.get_width()) / 2, (h - loosetext.get_height()) / 2))

        pygame.display.update()

        if not timevar:
            chrono = time.time()
            timevar = True
        if round(time.time() - chrono) > 4:

            color1 = (255, 0, 0)
            start = False
            ready = False
            playing = False
            myscore = 0
            timevar = False

            end = False




    screen.blit(cursor,(pygame.mouse.get_pos()[0]-24,pygame.mouse.get_pos()[1]-24))
    pygame.display.update()