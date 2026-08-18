intro=True


from time import sleep
import time
with open("config.py", "r") as file:

    config=eval(file.read())
    file.close()

workingdir=config["default directory"]

import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame, math, random, sys
import pygame.freetype
pygame.mixer.init()
pygame.freetype.init()
beep=pygame.mixer.Sound('audio/beep.wav')
beep.set_volume(0.001)
beepcount=0
print("Level Pack:")
a=input(":")
workingDir=a
print()
print("Level Number / Name")
a=input(":")
print(a)
try:

    a=eval(a)
except:
    a=a
print(a)
if type(a) is str:
    if a.endswith(".isketi"):
        print("added isketi")
        levelToEdit=a
    else:
        levelToEdit=f"{a}.isketi"
elif type(a) is int:
    levelToEdit=a
else:
    quit("you suck")
print(a)
def prin(text, timeSeconds=0.02):
    global beepcount
    for index in range(len(text)):
        print(text[index], end='', flush=True)
        beepcount+=1
        if beepcount>0:

            if text[index]!=" ":
                beep.set_volume(random.randint(75, 100)/5000)
                beep.play()
            beepcount=0
        sleep(timeSeconds)
    print()
def progressbar(before, percent, after):
    percentdisplay="|"

    for i in range(20):
        if i*5<=percent:
            percentdisplay+="#"
        else:
            percentdisplay+="-"
    percentdisplay+="|"
    sys.stdout.write(f"\r{before}  {percentdisplay} ({percent}%)  {after}")
    sys.stdout.flush()


pygame.init()
gravity=0.7
air_friction=0.95
borderBounce=-0.2
screenSizeOficial=[1920, 1080]
deaths=0


screen=pygame.display.set_mode(screenSizeOficial)

#import textures:

particleTexture=pygame.transform.scale(pygame.image.load('textures/wind.png').convert_alpha(), (30, 30))
holeTexture=pygame.image.load('textures/hole.png').convert_alpha()

#font treats:

fonts= {}
def load_font(size):
    global fonts
    if not size in fonts:
        fonts[size]=pygame.font.Font("textures/isketi.otf", size)
def text(words, size=40, color=(255, 255, 255)):
    if size in fonts:
        return fonts[size].render(words, True, color)
    load_font(size)
    return fonts[size].render(words, True, color)






#--------


icon=pygame.surface.Surface((50, 50), pygame.SRCALPHA)
icon.fill((255, 255, 255, 0))
pygame.display.set_icon(icon)
class fade:
    def __init__(self, fadetimeseconds, holdseconds):
        self.fadeby=255/(fadetimeseconds*60)
        self.holdtime=holdseconds*60
        self.holdwait=0
        self.fadeamount=255
    def tick(self):
        if self.holdwait>self.holdtime:
            self.fadeamount-=self.fadeby
        else:
            self.holdwait+=1
        return self.fadeamount


class notification:
    def __init__(self, x, y, image, fade, padding=10):
        if type(image) is pygame.surface.Surface:
            self.image=image
        else:
            print("Image must be pygame surface")
            quit(67)
        self.width=image.get_size()[0]
        self.height=image.get_size()[1]
        self.fade=fade
        self.done=False

        if type(x) is float or type(x) is int:
            self.x=x
        elif x=="l":
            self.x=padding
        elif x=="c":
            self.x=(screenSizeOficial[0]/2)-self.width/2
        elif x=="r":
            self.x=screenSizeOficial[0]-(self.width+padding)
        if type(y) is float or type(y) is int:
            self.y=y
        elif y=="t":
            self.y=padding
        elif y=="c":
            self.y=(screenSizeOficial[1]/2)-self.height/2
        elif y=="b":
            self.y=screenSizeOficial[1]-(self.height+padding)
    def draw(self):
        opacity=self.fade.tick()
        if opacity < 0:
            self.done=True
        else:
            self.image.set_alpha(opacity)
            screen.blit(self.image, (self.x, self.y))

def draw_line(p1, p2,color,  thickness=1):
    dx=p1[0]-p2[0]
    dy=p1[1]-p2[1]
    angle=math.atan2(dy, dx)
    wangle=angle+math.pi/2
    thickness/=2
    vector=(math.cos(wangle)*thickness, math.sin(wangle)*thickness)
    r1=(p1[0]+vector[0],p1[1]+vector[1])
    r2=(p2[0]+vector[0],p2[1]+vector[1])
    r3=(p2[0]-vector[0],p2[1]-vector[1])
    r4=(p1[0]-vector[0],p1[1]-vector[1])
    pygame.draw.polygon(screen, color, [r1, r2, r3, r4])
    pygame.draw.aaline(screen, color, r1, r2)
    pygame.draw.aaline(screen, color, r3, r4)
class fan:
    def __init__(self, x, y, angleNumber,  width, strength, particles=True, particle_amount=0.5):
        self.x=x
        self.y=y
        self.angleNumber=angleNumber
        self.strength=strength
        self.windStrength=strength/5
        self.particles=particles
        self.width=width
        self.particle_amount=1-particle_amount
        self.num=self.width*self.particle_amount

    def check(self, x, y, radius):
        pushed=False
        dist=0
        if self.angleNumber == 0:
            if x > self.x-radius and y > self.y-((self.width/2)+radius) and y< self.y+((self.width/2)+radius):
                pushed =True
                dist=abs(self.x-x)
        if self.angleNumber ==2:
            if x < self.x-radius and y > self.y-((self.width/2)+radius) and y< self.y+((self.width/2)+radius):
                pushed =True
                dist=-abs(self.x-x)
        if self. angleNumber ==3:
            if y < self.y-radius and x > self.x-((self.width/2)+radius) and x< self.x+((self.width/2)+radius):
                pushed =True
                dist=-abs(self.y-y)
        if self. angleNumber ==1:
            if y > self.y-radius and x > self.x-((self.width/2)+radius) and x< self.x+((self.width/2)+radius):
                pushed =True
                dist=abs(self.y-y)
        if pushed:

            strength= min(self.strength/(dist), 3)
            if self.angleNumber ==0 or self.angleNumber ==2:
                return [strength, 0]
            elif self.angleNumber ==1 or self.angleNumber ==3:
                return [0, strength]
            else:
                return[0, 0]
        else:
            return [0, 0]
    def tick(self):
        for i in range(25):
            if self.particles:
                if random.randint(0, self.width)>=self.num:
                    global wind
                    if self.angleNumber==0:
                        GAME.wind.append(particle(self.x, random.randint(self.y-round(self.width/2), self.y+round(self.width/2)),[self.windStrength, 0], particleTexture))
                    elif self.angleNumber==2:
                        GAME.wind.append(particle(self.x, random.randint(self.y - round(self.width / 2), self.y + round(self.width / 2)),[-self.windStrength, 0], particleTexture))
                    elif self.angleNumber==1:
                        GAME.wind.append(particle(random.randint(self.x - round(self.width / 2), self.x + round(self.width / 2)), self.y,[0, self.windStrength], particleTexture))
                    elif self.angleNumber==3:
                        GAME.wind.append(particle(random.randint(self.x - round(self.width / 2), self.x + round(self.width / 2)), self.y,[0, -self.windStrength], particleTexture))

class particle:
    def __init__(self, x, y, vector, image):
        self.x=x
        self.y=y
        self.vector=vector
        self.image=pygame.transform.rotate(image, random.randint(-180, 180))
        self.alpha=random.randint(180, 200)

    def draw(self):
        self.x+=self.vector[0]
        self.y+=self.vector[1]
        self.alpha-=3
        if self.alpha<0:
            global wind
            GAME.wind.remove(self)
        else:
            self.image.set_alpha(self.alpha)
            screen.blit(self.image, (self.x, self.y))






class hole:
    def __init__(self, x, y, strength):
        self.x=x
        self.y=y
        self.strength=strength

        self.texture=pygame.transform.scale(holeTexture, (strength*4, strength*4))
        self.grow=1
        self.growvelocity=0
        self.offset=[0, 0]
        self.offsetvelocity=[0, 0]
    def attractPoints(self, points):
        index=0
        dead=[]
        for point in points:
            dx=self.x-point.x
            dy=self.y-point.y
            dist=math.sqrt(dx**2+dy**2)
            if dist<self.strength:
                dead.append(index)
            angle=math.atan2(dy,dx)
            force=min((self.strength/max(dist, 10)**1.3 )*50, 25)
            point.push(math.cos(angle)*force, math.sin(angle)*force)
            index+=1
        return dead
    def draw(self):

        self.growvelocity-=(self.grow-1)/20
        if random.randint(0, 4)==4:
            self.growvelocity+=random.randint(-1, 1)/100
        self.grow+=self.growvelocity
        self.growvelocity*=air_friction


        self.offsetvelocity[0]-=(self.offset[0])/20
        self.offsetvelocity[1]-=(self.offset[1])/20
        if random.randint(0, 4)==4:
            self.offsetvelocity[0]+=random.randint(-1, 1)/100
        if random.randint(0, 4)==4:
            self.offsetvelocity[1]+=random.randint(-1, 1)/100
        self.offset[0]+=self.offsetvelocity[0]
        self.offset[1]+=self.offsetvelocity[1]
        self.offsetvelocity[0]*=air_friction
        self.offsetvelocity[1]*=air_friction



        self.texture.set_alpha(random.randint(200, 255))
        screen.blit(self.texture, (self.x-(self.texture.get_size()[0]/2)+self.offset[0], self.y-(self.texture.get_size()[1]/2)+self.offset[1]))
        pygame.draw.circle(screen, (0, 0, 0), (self.x+self.offset[0], self.y+self.offset[1]), self.strength*self.grow)
def drawRects(rects):
    for rect in rects:
        rect.draw()

def connectPoints(p1, p2, distance, elasticity=0.5):
    dx=p2.x-p1.x
    dy=p2.y-p1.y
    dist=math.sqrt(dx**2+dy**2)
    dist-=distance
    dist*=elasticity
    dist=min(dist, 4)
    angle=math.atan2(dy,dx)
    dx=math.cos(angle)*dist
    dy=math.sin(angle)*dist
    p1.push(dx,dy)
    p2.push(-dx,-dy)
def mix_colors(col1, col2, amount):
    r=((1-amount)*col1[0])+(amount*col2[0])
    g=((1-amount)*col1[1])+(amount*col2[1])
    b=((1-amount)*col1[2])+(amount*col2[2])
    return(r, g, b)
class connectedObject:
    def __init__(self, points, radius, color, connections, elasticity=0.5, polygon=[]):
        self.balls=[]
        self.alive=True
        self.inFluid=0
        self.elasticity=elasticity
        self.elasticityStore=elasticity
        self.color=color
        self.interact_color=(255, 255, 255)
        self.dotColor=(255-self.color[0], 255-self.color[1], 255-self.color[2])
        self.original_color=color
        self.colormerge=0
        self.radius=radius
        self.polygon=polygon
        self.groundedCount=0
        self.end=False
        for point in points:
            self.balls.append(ball(point[0], point[1], radius, self.dotColor))
        self.connections=connections
        for connection in self.connections:
            if len(connection)<3:
                dx=abs(self.balls[connection[0]].x-self.balls[connection[1]].x)
                dy=abs(self.balls[connection[0]].y-self.balls[connection[1]].y)
                connection.append(math.sqrt(dx**2+dy**2))
    def tick(self):
        if self.alive:
            self.elasticity=self.elasticityStore
        else:
            self.elasticity=0.06
        self.inFluid=0
        for connection in self.connections:
            connectPoints(self.balls[connection[0]], self.balls[connection[1]], connection[2], self.elasticity)
        self.groundedCount=0
        for h in GAME.holes:
            buff= h.attractPoints(self.balls)
            for i in buff:
                self.balls[i].health-=50
        self.end=True
        for dot in self.balls:
            dot.tick()
            if dot.grounded:
                self.groundedCount+=1

            if dot.inFluid:
                self.inFluid+=1
            if GAME.has_end_position:
                if dot.end_distance>GAME.end_distance:
                    self.end=False
        if self.end:
            self.colormerge+=(1-self.colormerge)/10

        else:
            self.colormerge += (0 - self.colormerge) / 10
        self.colormerge=min(max(self.colormerge, 0), 1)
    def draw(self):
        self.color=mix_colors(self.original_color, self.interact_color, self.colormerge)
        if len(self.polygon) > 2:
            polybuffer=[]
            colorBuffer=(self.color[0], self.color[1], self.color[2])
            for treat in self.polygon:
                polybuffer.append((self.balls[treat].x, self.balls[treat].y))
            #colorBuffer = (self.color[0] * random.randint(70, 100)/100,
                           #self.color[1] * random.randint(70, 100)/100,
                           #self.color[2] * random.randint(70, 100)/100)
            pygame.draw.polygon(screen, colorBuffer, polybuffer)
            for dot in polybuffer:
                pygame.draw.circle(screen, colorBuffer, dot, self.radius)
            for i in range(len(polybuffer)):
                if i==0:
                    #pygame.draw.line(screen, colorBuffer, polybuffer[0], polybuffer[len(polybuffer)-1], 18)
                    draw_line(polybuffer[0], polybuffer[len(polybuffer)-1], colorBuffer, 10)
                else:
                    #pygame.draw.line(screen, colorBuffer, polybuffer[i-1], polybuffer[i], 18)
                    draw_line(polybuffer[i-1], polybuffer[i], colorBuffer, 10)

        else:
            for connection in self.connections:
                colorBuffer=(self.color*random.randint(0.70, 1)*self.color[0], self.color*random.randint(0.70, 1)*self.color[1], self.color*random.randint(0.70, 1)*self.color[2])
                pygame.draw.line(screen, colorBuffer, (self.balls[connection[0]].x, self.balls[connection[0]].y), (self.balls[connection[1]].x, self.balls[connection[1]].y))
        for dot in self.balls:
            dot.draw()



    def push(self, x, y, requirement=None):
        if requirement==None:
            for dot in self.balls:
                dot.push(x, y)
        elif requirement == "fluid":
            for dot in self.balls:
                if dot.inFluid:
                    dot.push(x, y)

transition=0

transition_change=0

transition_surface=pygame.Surface((screenSizeOficial[0],screenSizeOficial[1]), pygame.SRCALPHA)

redness=0

holding=-1
def drag(mousePos, mousePosPrev, mouse, mouseprev):
    global holding
    if holding>-1:
        if mouse:
            h=GAME.player.balls[holding]
            GAME.player.push((mousePos[0] - h.x) / 60, (mousePos[1] - h.y) / 60)
            h.setPos(mousePos[0], mousePos[1])
            h.xvel=0
            h.yvel=0


        else:
            holding=-1
    else:
        if mouse and not mouseprev:
            for i, b in enumerate(GAME.player.balls):
                if abs(b.x-mousePos[0])<= b.radius and abs(b.y-mousePos[1])<= b.radius:
                    holding=i





def transitionTick():
    global transition
    global transition_change
    global transition_surface
    global redness
    global deaths

    transition-=transition_change

    if transition<0:
        transition=0
    if transition>1:
        transition=1
    if transition_change!=0:
        transition_surface.fill((255, 255, 255, transition*255))
    if transition==0:
        transition_change=0
        if not GAME.player.alive:
            redness+=1
            transition_surface.fill((250, 40, 25, min(redness, 255)))
            screen.blit(transition_surface, (0, 0))
            if redness>255:
                redness=0
                transitionStart(2)
                GAME.respawn(GAME.levelNumber)
                deaths+=1
                GAME.notifications.append(notification("l", "t", text(f"Deaths: {deaths}", 40),fade(3, 3), 20))


    else:
        screen.blit(transition_surface, (0, 0))


def transitionStart(length):
    global transition
    global transition_change
    transition_change=1/(60*length)
    transition=1


class rect:
    def __init__(self, x, y, width, height, color, bounce=-0.5, friction=0.8, kills=False, fluid=False):
        self.x = x
        self.y = y
        self.fluid=fluid
        self.width = width
        self.height = height
        self.kills=kills
        self.color = color
        self.bounce = bounce
        self. friction = friction
    def draw(self):
        pygame.draw.rect(screen, self.color, [self.x, self.y, self.width, self.height])
class collisionData:
    def __init__(self):
        self.collision=False
        self.moveX=0
        self.fluid=False
        self.moveY=0
        self.bounceX=1
        self.bounceY=1
        self.index=-1
        self.kills=False
        self.frictionx=1
        self.frictiony=1
        self.colidedy=False
        self.colidedx=False
        self.collidedborder=False
def collisionDetect(x,y,radius, ignore=[]):
    output=collisionData()
    screenSize=[screenSizeOficial[0]-radius,screenSizeOficial[1]-radius]
    if x>screenSize[0]:

        output.collision=True
        output.colidedborder=True
        output.moveX=screenSize[0]-x
        output.bounceX=borderBounce
    elif y > screenSize[1]:

        output.collision = True
        output.colidedborder = True
        output.moveY =  screenSize[1]-y
        output.bounceY = borderBounce
    elif x<radius:
        output.colidedborder = True
        output.collision=True
        output.moveX=radius-x
        output.bounceX=borderBounce
    elif y<radius:
        output.colidedborder = True
        output.collision=True
        output.moveY=radius-y
        output.bounceY=borderBounce
    index = 0
    for rect in GAME.rects:
        if output.collision:
            break
        rect.x-=radius
        rect.y-=radius
        rect.width+=radius*2
        rect.height+=radius*2

        if x>rect.x and x<rect.x+rect.width and y>rect.y and y<rect.y+rect.height and not index in ignore:

            output.collision=True
            output.kills=rect.kills
            output.index=index
            if not rect.fluid:
                dx=(rect.x-x, (rect.x+rect.width)-x)
                dy=(rect.y-y, (rect.y+rect.height)-y)
                if abs(dx[0])>abs(dx[1]):
                    dx=dx[1]
                else:
                    dx=dx[0]
                if abs(dy[0])>abs(dy[1]):
                    dy=dy[1]
                else:
                    dy=dy[0]
                if abs(dx)>abs(dy):
                    output.moveY=dy
                    output.bounceY=rect.bounce
                    output.frictionx=rect.friction
                    output.colidedy=True
                else:
                    output.moveX=dx
                    output.bounceX=rect.bounce
                    output.frictiony=rect.friction
                    output.colidedx=True
            else:

                output.fluid=True
                output.frictionx=rect.friction
                output.frictiony=rect.friction
                output.moveX=0
                output.moveY=0
                output.bounceX=1
                output.bounceY=1
        index+=1
        rect.x += radius
        rect.y += radius
        rect.width -= radius * 2
        rect.height -= radius * 2
    return output

class ball:
    def __init__(self, x, y, radius, color=(255, 255, 255)):
        self.x = x
        self.y = y
        self.inFluid=False
        self.alive=True
        self.health=100
        self.yvel=0
        self.xvel=0
        self.radius = radius
        self.color = color
        self.grounded=False
        self.end_distance=10000
    def tick(self):
        global GAME
        self.health+=1
        self.health=min(self.health, 100)
        self.grounded=False
        self.inFluid=False
        if self.health<=0:
            self.alive=False
        for fan in GAME.fans:
            push=fan.check(self.x, self.y, self.radius)
            self.push(push[0], push[1])

        self.yvel+=gravity

        self.xvel*=air_friction

        self.yvel*=air_friction

        self.x+=self.xvel

        self.y+=self.yvel
        colidedWith=[]
        collisionbuffer=collisionDetect(self.x, self.y, self.radius)
        safety=0
        while collisionbuffer.collision and safety<10:
            if collisionbuffer.kills:
                self.alive=False
            if collisionbuffer.fluid:
                self.inFluid=True
                colidedWith.append(collisionbuffer.index)
                #print(collisionbuffer.index)

            self.x+=collisionbuffer.moveX

            self.y+=collisionbuffer.moveY

            if collisionbuffer.moveY<0:
                self.grounded=True

            self.xvel*=collisionbuffer.bounceX

            self.yvel*=collisionbuffer.bounceY

            self.xvel*=collisionbuffer.frictionx

            self.yvel*=collisionbuffer.frictiony

            collisionbuffer=collisionDetect(self.x, self.y, self.radius, colidedWith)
            safety+=1
        if GAME.has_end_position:
            endx=self.x-GAME.end_position[0]
            endy=self.y-GAME.end_position[1]
            self.end_distance=math.sqrt((endx**2)+(endy**2))
    def draw(self):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)
    def push(self, x, y):
        self.xvel+=x
        self.yvel+=y
    def setPos(self, x, y):
        self.x=x
        self.y=y
def keypressed(name):
    return eval(f"keys[pygame.K_{name}]")

#IMPORTING JUNK-------------------------------------------------------------------------
sket={}

class game:
    def __init__(self):
        self.level_loaded=""
        self.levelNumber=0
        self.rects=[]
        self.holes=[]
        self.fans=[]
        self.wind=[]
        self.notifications=[]
        self.draw_rects=False
        self.draw_holes=False
        self.draw_fans=False
        self.bglayer=False
        self.lighting=False
        self.player=0
        self.saveData=[]
        self.has_end_position=False
        self.end_position=[0, 0]
        self.end_distance=0
    def unload(self):
        self.level_loaded = ""
        self.rects = []
        self.holes = []
        self.fans = []
        self.wind = []
        self.notifications=[]
        self.bglayer = False
        self.lighting = False
        self.has_end_position = False
        self.end_position = [0, 0]
        self.end_distance = 0
    def respawn(self, level):
        print(f"Respawning Character from save file: {self.levelNumber}")
        l=self.saveData[self.levelNumber]

        for b in range(len(self.player.balls)):
            self.player.balls[b].alive=True
            self.player.balls[b].health=100
            self.player.balls[b].x=l[b][0]
            self.player.balls[b].y = l[b][1]
            self.player.balls[b].xvel = 0
            self.player.balls[b].xvel = 1
        self.player.alive=True
    def save(self):
        print("Saving Player Position Data")
        savebuff=[]
        for b in self.player.balls:
            savebuff.append([b.x, b.y])
        self.saveData.append(savebuff)
        print(f"sucesfully filled save slot: {len(self.saveData)-1}")
    def load(self,path):
        print(f"Started Loading:{path}")
        self.level_loaded = path
        self.levelNumber=sket["levels"].index(path)
        lvl = {}

        with open(f"{workingdir}/{path}", "r") as file:
            lvl = (eval(file.read()))
            file.close()
        if "name" in lvl:
            self.notifications.append(notification("c", 100, text(lvl["name"], 100, (255, 255, 255)), fade(10, 5)))
        if "end_position" in lvl:
            self.end_position=lvl["end_position"]
        else:
            print("No End Position Found")
        if "rects" in lvl:
            self.rectbuff = lvl["rects"]
        if "holes" in lvl:
            self.holebuff = lvl["holes"]
        if "fans" in lvl:
            self.fanbuff = lvl["fans"]
        if "end_position" in lvl:
            self.end_position = lvl["end_position"]
            self.has_end_position = True
            self.end_distance=50 if not "end_distance" in lvl else lvl["end_distance"]
        else:
            self.has_end_position = False
        for r in self.rectbuff:
            self.add_rect(r)
            print(f"Successfully Loaded Rectangle: {r}")
        for h in self.holebuff:
            self.add_hole(h)
            print(f"Successfully Loaded Black Hole: {h}")
        for f in self.fanbuff:
            self.add_fan(f)
            print(f"Successfully Loaded Fan: {f}")
        self.bglayer=False if not "base" in lvl else pygame.image.load(f"{workingdir}/{lvl["base"]}").convert()
        self.lighting=False if not "light" in lvl else pygame.image.load(f"{workingdir}/{lvl["light"]}").convert_alpha()
        if self.bglayer!=False:
            self.bglayer=pygame.transform.scale(self.bglayer, sket["size"])
        if self.lighting!=False:
            self.lighting=pygame.transform.scale(self.lighting, sket["size"])
    def add_rect(self, r):
        rec = r["rect"]
        colo = (255, 255, 255) if not "color" in r else r["color"]
        bounc = 0 if not "bounce" in r else r["bounce"]
        frictio = 0.5 if not "friction" in r else r["friction"]
        kill = False if not "kills" in r else r["kills"]
        fluid=False if not "fluid" in r else r["fluid"]
        self.rects.append(rect(rec[0], rec[1], rec[2], rec[3], colo, bounc, frictio, kill, fluid))
    def add_hole(self, h):
        pos=h["pos"]
        str = 20 if not "strength" in h else h["strength"]
        self.holes.append(hole(pos[0], pos[1], str))
    def add_fan(self, f):
        pos=f["pos"]
        width = f["width"]
        str = f["strength"]
        angle = f["angle"]
        part=True if not "particles" in f else f["particles"]
        partamm = 0.6 if not "particle_amount" in f else f["particle_amount"]
        self.fans.append(fan(pos[0], pos[1], angle, width, str, part, partamm))
    def game_tick(self):
        self.player.tick()
        for f in self.fans:
            f.tick()
    def game_draw(self):
        if self.bglayer !=False:
            screen.blit(self.bglayer, (0, 0))

        if self.draw_fans:
            for f in self.fans:
                f.draw()
        if self.draw_rects:
            for r in self.rects:
                r.draw()
        self.player.draw()
        for p in self.wind:
            p.draw()


        if self.draw_holes:
            for h in self.holes:
                h.draw()


        if self.lighting!=False:

            screen.blit(self.lighting, (0, 0))
            if random.randint(0, 5)==5:
                self.lighting.set_alpha(random.randint(0, 25))
                screen.blit(self.lighting, (0, 0))
                self.lighting.set_alpha(255)

        for notif in self.notifications:
            notif.draw()
            if notif.done:
                self.notifications.remove(notif)

GAME=game()

with open(f"{workingdir}/set.sket", "r") as file:
    sket=eval(file.read())
    file.close()
if "size" in sket:
    screenSizeOficial=sket["size"]
else:
    screenSizeOficial=[1920, 1080]
if type(levelToEdit) is int:
    sket["levels"]=sket["levels"][levelToEdit]
else:
    sket["levels"]=[levelToEdit]


pygame.display.set_caption(sket["title"])

GAME.draw_rects= True
GAME.draw_holes= True
GAME.draw_fans = True

levelNumber=0
levelList=[]
if "levels" in sket:
    levelList=sket["levels"]
else:
    quit("missing levels vro :(")

def level_tick():

    if GAME.level_loaded!=sket["levels"][GAME.levelNumber]:
        print("changing level")
        GAME.save()
        GAME.unload()
        GAME.load(sket["levels"][GAME.levelNumber])















#-----------------------------------------------------------------------------------------

clock=pygame.time.Clock()

#game loop:




import textures







#other stuff------------------

jumpwait=0
if "startX" in sket:
    startX=sket["startX"]
else:
    startX=0
if "startY" in sket:
    startY=sket["startY"]
else:
    startY=0

points=[[120, 30], [140, 30], [160, 30], [180, 30], [200, 30], [120, 50], [140, 50], [160, 50], [180, 50], [200, 50], [120, 70], [140, 70], [160, 70], [180, 70], [200, 70], [120, 90], [140, 90], [160, 90], [180, 90], [200, 90], [120, 110], [140, 110], [160, 110], [180, 110], [200, 110]]
print(points)
points=[[0+startX, 0+startY],[20+startX, 0+startY],[40+startX, 0+startY],[60+startX, 0+startY],[80+startX, 0+startY],[0+startX, 20+startY],[20+startX, 20+startY],[40+startX, 20+startY],[60+startX, 20+startY],[80+startX, 20+startY],[0+startX, 40+startY],[20+startX, 40+startY],[40+startX, 40+startY],[60+startX, 40+startY],[80+startX, 40+startY],[0+startX, 60+startY],[20+startX, 60+startY],[40+startX, 60+startY],[60+startX, 60+startY],[80+startX, 60+startY],[0+startX, 80+startY],[20+startX, 80+startY],[40+startX, 80+startY],[60+startX, 80+startY],[80+startX, 80+startY]]
print(points)
connections=[[0, 1], [0, 5], [0, 6], [1, 2], [1, 6], [1, 7], [1, 5], [2, 3], [2, 7], [2, 8], [2, 6], [3, 4], [3, 8], [3, 9], [3, 7], [4, 9], [4, 8], [5, 6], [5, 10], [5, 11], [6, 7], [6, 11], [6, 12], [6, 10], [7, 8], [7, 12], [7, 13], [7, 11], [8, 9], [8, 13], [8, 14], [8, 12], [9, 14], [9, 13], [10, 11], [10, 15], [10, 16], [11, 12], [11, 16], [11, 17], [11, 15], [12, 13], [12, 17], [12, 18], [12, 16], [13, 14], [13, 18], [13, 19], [13, 17], [14, 19], [14, 18], [15, 16], [15, 20], [15, 21], [16, 17], [16, 21], [16, 22], [16, 20], [17, 18], [17, 22], [17, 23], [17, 21], [18, 19], [18, 23], [18, 24], [18, 22], [19, 24], [19, 23], [20, 21], [21, 22], [22, 23], [23, 24], [0, 2], [0, 10], [0, 12], [1, 3], [1, 11], [1, 13], [2, 4], [2, 12], [2, 14], [2, 10], [3, 13], [3, 11], [4, 14], [4, 12], [5, 7], [5, 15], [5, 17], [6, 8], [6, 16], [6, 18], [7, 9], [7, 17], [7, 19], [7, 15], [8, 18], [8, 16], [9, 19], [9, 17], [10, 12], [10, 20], [10, 22], [11, 13], [11, 21], [11, 23], [12, 14], [12, 22], [12, 24], [12, 20], [13, 23], [13, 21], [14, 24], [14, 22], [15, 17], [16, 18], [17, 19], [20, 22], [21, 23], [22, 24], [0, 3], [0, 15], [0, 18], [1, 4], [1, 16], [1, 19], [2, 17], [3, 18], [3, 15], [4, 19], [4, 16], [5, 8], [5, 20], [5, 23], [6, 9], [6, 21], [6, 24], [7, 22], [8, 23], [8, 20], [9, 24], [9, 21], [10, 13], [11, 14], [15, 18], [16, 19], [20, 23], [21, 24]]
draw=[0, 1, 2, 3, 4, 9, 14, 19, 24, 23, 22, 21, 20, 15, 10, 5]

if "custompoints" in sket:
    points=sket["custompoints"]
if "customconnections" in sket:
    connections=sket["customconnections"]
if "customdraw" in sket:
    draw=sket["customdraw"]
if "elasticity" in sket:
    elasticity=sket["elasticity"]
else:
    elasticity=0.08
if "customcolor" in sket:
    color=sket["customcolor"]
else:
    color=(255, 100, 255)
if "customradius" in sket:
    radius=sket["customradius"]
else:
    radius=5
GAME.player=connectedObject(points, radius, color,
    connections, elasticity=elasticity, polygon=draw)
#GAME.save()

running=True
transitionStart(2)
keys=pygame.key.get_pressed()
prevkeys=pygame.key.get_pressed()
level_tick()
w_count=0
GAMESTARTTIME=time.time()
GAMERUNTIME=0
moved=False
mouse=pygame.mouse.get_pressed(3)[0]
mousePos=pygame.mouse.get_pos()


tool=0
tools=["select", "move", "draw rectangles"]













while running:
    GAMERUNTIME=time.time()-GAMESTARTTIME
    level_tick()



    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running=False
    keys = pygame.key.get_pressed()
    mousePrev=mouse
    mouse=pygame.mouse.get_pressed(3)[0]
    mousePosPrev=mousePos
    mousePos=pygame.mouse.get_pos()
    if keypressed("ESCAPE"):
        running=False
    jumpwait-=1


    if not moved and GAMERUNTIME>10 and GAMERUNTIME<10.02:
        GAME.notifications.append(notification("r", "t", pygame.image.load("textures/move.png").convert_alpha(), fade(4, 4), 20))



    if jumpwait<0:
        jumpwait=0
    if GAME.player.alive:
        if keypressed("a"):
            moved=True
            GAME.player.push(-0.5, 0)
            if GAME.player.groundedCount>1:
                GAME.player.push(-0.5, 0)
        if keypressed("d"):
            moved = True
            GAME.player.push(.5, 0)
            if GAME.player.groundedCount>1:
                GAME.player.push(0.5, 0)
        if keypressed("w"):

            w_count+=1
            if GAME.player.groundedCount>2 and jumpwait==0 and w_count<10:
                moved = True
                GAME.player.push(0, -23)
                jumpwait=10
            elif GAME.player.inFluid>3 and jumpwait==0:
                moved = True
                GAME.player.push(0, -4, "fluid")
        else:
            w_count=0
        if keypressed("s"):
            moved = True
            GAME.player.push(0, 0.5)
        if keypressed("r")and not prevkeys[pygame.K_r]:
            redness = 0
            transitionStart(2)
            GAME.respawn(GAME.levelNumber)
        if keypressed("SPACE")and not prevkeys[pygame.K_SPACE] and GAME.player.end:


            transitionStart(2)
            GAME.levelNumber+=1



    drag(mousePos, mousePosPrev, mouse, mousePrev)





    screen.fill((0, 0, 0))

    GAME.game_tick()
    GAME.game_draw()


    #drawRects()


    #for p in wind:
    #    p.draw()

    clock.tick(60)
    #screen.blit(font.render(f"fps: {round(clock.get_fps())}", True, (255, 255, 255)), (10, 10))
    transitionTick()





    if keypressed("p") and not prevkeys[pygame.K_p]:
        pygame.image.save(screen, "screenshot.png")

    pygame.display.flip()
    prevkeys=keys

