import pygame
import sys
import math
import numpy as np
from numba import *
from numba.experimental import *
import random

class GameState():
    def __init__(self,game):
        self.state="Level_1"
        self.game=game
    #Level 1 State
    def level_1(self):
        #self.game.draw_text('1_Placeholder_1',20,self.game.DISPLAY_W/2,self.game.DISPLAY_H/2)
        self.nf()
        self.game.display=pygame.surfarray.make_surface(self.game.frame*255)
        self.game.display=pygame.transform.scale(self.game.display,(800,600))
        if self.game.K_E:
            self.state="Level_2"
    #Level 2 State
    def level_2(self):
        self.game.draw_text('2_Placeholder_2',20,self.game.DISPLAY_W/2,self.game.DISPLAY_H/2)   
    #State handler
    def state_manager(self):
        if self.state=="Level_1":
            self.level_1()
        if self.state=="Level_2":
            self.level_2()
    #Camera vision loop, creates 60 fov render
    def nf(self):
        DISPLAY_W=self.game.DISPLAY_W
        HALFVRES=self.game.HALFVRES
        rot=self.game.rot
        mod=self.game.mod
        frame=self.game.frame
        maph=self.game.maph
        size=self.game.size
        posx,posy=self.game.posx,self.game.posy
        frame=self.new_frame(DISPLAY_W,HALFVRES,rot,mod,frame,posx,posy,maph,size)
    @staticmethod
    @njit()
    def new_frame(DISPLAY_W,HALFVRES,rot,mod,frame,posx,posy,maph,size):
        for i in range(DISPLAY_W):
            rot_i=rot+np.deg2rad(i/mod-30)
            sin,cos,cos2=np.sin(rot_i),np.cos(rot_i),np.cos(np.deg2rad(i/mod-30))
            for j in range(HALFVRES):
                n=(HALFVRES/(HALFVRES-j))/cos2
                x,y=posx+cos*n,posy+sin*n
                #---
                if maph[int(x)%(size-1)][int(y)%(size-1)]:
                    h=HALFVRES-j
                    r=random.randint(1,2)
                    if r==1:
                        c=[0,1,0]
                    if r==2:
                        c=[0,0,0]
                    for k in range(h*2):
                        frame[i][HALFVRES-h+k]=c
                    break
                else:
                    #--- Floor & Ceiling
                    if int(x)%2==int(y)%2:
                        frame[i][HALFVRES*2-j-1]=[0.5,0.5,0.5]
                        frame[i][j]=[1,1,1]
                    else:
                        frame[i][HALFVRES*2-j-1]=[1,1,1]
                        frame[i][j]=[0.2,0.2,0.2]
        return frame
    def movement(self,posx,posy,rot,keys,dt):
        x,y=(posx,posy)
        if keys[pygame.K_LEFT] or keys[ord("a")]:
            rot=rot-0.1*dt
        if keys[pygame.K_RIGHT] or keys[ord("d")]:
            rot=rot+0.1*dt
        if keys[pygame.K_UP] or keys[ord("w")]:
            x,y=(x+dt*np.cos(rot),y+dt*np.sin(rot))
        if keys[pygame.K_DOWN] or keys[ord("s")]:
            x,y=(x-dt*np.cos(rot),y-dt*np.sin(rot))
        posx,posy=(x,y)
        return posx,posy,rot    