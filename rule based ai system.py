import pygame as p
import random as r
import sys
import math as m
import time

# python library intialize
p.init()

# Set screen and caption
screen=p.display.set_mode((600,600))
p.display.set_caption("Rule based AI")

# Colors
black=(0,0,0)
red=(255,0,0)
green=(0,255,0)
blue=(0,0,255)

# game variable
run=True
increse_axis=2
clock=p.time.Clock()
speed=2
object=[]
fps=60
q=2
top_y=30
x_scalen=150
y_scalen=30
score=0
Font=p.font.SysFont("Arial",32)
circle_x=300
circle_y=400
radius=20
move_right=True
move_left=False
ai_Fails=0
last_sec=0

# player variable
player_x=350
player_y=300
player_fail=0
player_radius=20
lastsec=0

# game loop
while run:
    for event in p.event.get():
        if event.type==p.QUIT:
            run=False
        if event.type==p.KEYDOWN:
            if event.key==p.K_q:
                run=False
    
    # for button control
    key=p.key.get_pressed()
    if key[p.K_LEFT] and player_x>radius:
        player_x-=20
    if key[p.K_RIGHT] and player_x<600-radius:
        player_x+=20
    if key[p.K_DOWN] and player_y<600-radius:
        player_y+=20
    if key[p.K_UP] and player_y>radius:
        player_y-=20
    
    # generating obstecle 
    q+=1
    if q%fps==0:
                object.append(
                {'x':r.randint(10,450),
                'y':top_y,
                'x_scale':x_scalen,
                'y_scale':y_scalen})
    screen.fill(black)

    # ploting obstecle
    for o in object:
        rect = p.Rect(o['x'], o['y'], o['x_scale'], o['y_scale'])
        p.draw.rect(screen,red,(o['x'],o['y'],o['x_scale'],o['y_scale']),20)
        o['y']+=2
        if o['y']>600:
            object.remove(o)
            score+=1
        
        # AI Distance calculation
        closest_x=max(rect.left,min(circle_x,rect.right))
        closest_y=max(rect.top,min(circle_y,rect.bottom))
        dx=circle_x-closest_x
        dy=circle_y-closest_y
        distance=m.sqrt(dx*dx+dy*dy)

        # Rule for AI to move Right
        if move_right:
            if distance<radius+45:
                circle_x+=20
                if circle_x>580:
                    move_right=False
                    move_left=True
        
        # Rule for AI to move Left
        if move_left:
            if distance<radius+45:
                circle_x-=20
                if circle_x<40:
                    move_left=False
                    move_right=True

        # Count only 1 loose in last 1 sec for AI
        currenttiem=p.time.get_ticks()
        if distance<radius:
            if currenttiem-last_sec>1000:
                ai_Fails+=1
                last_sec=currenttiem


        # player distance calculation
        pclosest_x=max(rect.left,min(player_x,rect.right))
        pclosest_y=max(rect.top,min(player_y,rect.bottom))
        pdx=player_x-pclosest_x
        pdy=player_y-pclosest_y
        pdistance=m.sqrt(pdx*pdx+pdy*pdy)

        # Count only 1 loose in last 1 sec for player
        current_tiem=p.time.get_ticks()
        if pdistance<player_radius:
            if current_tiem-lastsec>1000:
                player_fail+=1
                lastsec=current_tiem

    # Total Score
    text=Font.render(f"Score:{score}",True,(255,255,255))
    screen.blit(text,(20,20))

    # AI Looses Score
    ai_loos=Font.render(f"Ai Looses:{ai_Fails}",True,(255,255,255))
    screen.blit(ai_loos,(150,20))

    # AI
    p.draw.circle(screen,red,(circle_x,circle_y),radius)
    
    # player
    p.draw.circle(screen,blue,(player_x,player_y),player_radius)

    # Player Looses Score
    human_loose=Font.render(f"Your looses:{player_fail}",True,(255,255,255))
    screen.blit(human_loose,(330,20))
    
    # update screen and control fps
    p.display.flip()
    clock.tick(60)

# Destroy python object
p.quit()