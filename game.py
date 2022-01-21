import random
h=720
w=1280
class Game:
    def __init__(self):
        self.name="P"
        self.pos= {}
        self.ball=[w/2,h/2]
        self.ready=0
        self.start=False
        self.end=False
    def changepos(self):
        if self.name=="P":
            self.ball[0]=random.randrange(0+71,w-71)
            self.ball[1]=random.randrange(0,h-62)
        else:
            self.ball[0] = random.randrange(0 + 35, w- 35)
            self.ball[1] = random.randrange(0, h - 31)
    def changeball(self):
        self.name=random.choice("MPPPPPPPPPP")
    def reset(self):
        self.name = "P"

        self.ball = [w / 2, h / 2]
        self.ready=0

        self.start = False
        self.end = False