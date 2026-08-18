avgSize=[1920, 1080]
b=input("width")
if b =="":
    width=avgSize[0]
else:
    width=int(b)
b = input("height")
if b =="":
    height=avgSize[1]
else:
    height=int(b)
i = input("add too:")
import pygame
pygame.init()
if i =="":
    rects=[]
else:
    rects=[]



    for r in eval(i):
        rects.append(r["rect"])
i=input("background path")
screen=pygame.display.set_mode((width,height))
if i =="":
    background=pygame.Surface((width, height))
else:
    background=pygame.transform.scale(pygame.image.load(i).convert(), (width, height))



pygame.display.set_caption("rect drawer")
font=pygame.font.Font(None, 20)
selected=-1
writing=-1
click=pygame.mouse.get_pressed(3)
prevclick=click
#rects=[]
index=0
def drawRect(index):
    if index==writing:
        #print([[rects[index][0], rects[index][1]], [rects[index][0]+rects[index][2], rects[index][1]], [rects[index][0]+rects[index][2], rects[index][1]+rects[index][3]], [rects[index][0], rects[index][1]+rects[index][3]]])
        pygame.draw.lines(screen, (250, 100, 250), True, [[rects[index][0], rects[index][1]], [rects[index][0]+rects[index][2], rects[index][1]], [rects[index][0]+rects[index][2], rects[index][1]+rects[index][3]], [rects[index][0], rects[index][1]+rects[index][3]]], 1)
    else:
        if selected==index:

            pygame.draw.rect(screen, (255, 255, 255), rects[index])
        else:
            pygame.draw.rect(screen, (250, 250, 100), rects[index])
        pygame.draw.lines(screen, (255, 100, 100), True,[[rects[index][0], rects[index][1]], [rects[index][0]+rects[index][2], rects[index][1]], [rects[index][0]+rects[index][2], rects[index][1]+rects[index][3]], [rects[index][0], rects[index][1]+rects[index][3]]], 1)
def out():
    buff=[]
    for rect in rects:
        buff.append({"rect":rect})
    print(buff)
running=True
keys=pygame.key.get_pressed()
prevkeys=keys
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running=False
    click = pygame.mouse.get_pressed(3)
    keys = pygame.key.get_pressed()

    if click[0] and  not prevclick[0]:

        if writing == -1:
            writing=len(rects)
            rects.append([pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], 0, 0])

            print("added rectangle")
        else:
            rects[writing][2]=pygame.mouse.get_pos()[0]-rects[writing][0]
            rects[writing][3]=pygame.mouse.get_pos()[1]-rects[writing][1]
            writing=-1
            print("finished rectangle")

    else:
        if writing != -1:
            rects[writing][2] = pygame.mouse.get_pos()[0]-rects[writing][0]
            rects[writing][3] = pygame.mouse.get_pos()[1]-rects[writing][1]
    if keys[pygame.K_SPACE] and not prevkeys[pygame.K_SPACE]:
        if selected==-1:
            if writing != -1:
                selected=len(rects)-2
            else:
                selected=len(rects)-1
        else:
            selected-=1
            if selected==-1:
                if writing != -1:
                    selected = len(rects) - 2
                else:
                    selected = len(rects) - 1
    if keys[pygame.K_BACKSPACE] and not prevkeys[pygame.K_BACKSPACE]:
        if selected==-1:
            if writing != -1:
                rects.remove(rects[len(rects)-2])
            else:
                rects.remove(rects[len(rects)-1])
        else:
            rects.remove(rects[selected])
    if keys[pygame.K_RETURN] and not prevkeys[pygame.K_RETURN]:
        selected=-1
    screen.blit(background, (0, 0))
    if keys[pygame.K_p] and not prevkeys[pygame.K_p]:
        out()


    for i in range(len(rects)):
        drawRect(i)
    prevclick = click
    pygame.display.flip()
    prevkeys = keys
pygame.quit()
