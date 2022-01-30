import pygame
import sys
import math
import numpy as np

class GameState():
    def __init__(self,game):
        self.state="Level_1"
        self.game=game
    #Level 1 State
    def level_1(self):
        #self.game.draw_text('1_Placeholder_1',20,self.game.DISPLAY_W/2,self.game.DISPLAY_H/2)
        self.sky=pygame.image.load("skybox.jpg")
        self.sky=pygame.surfarray.array3d(pygame.transform.scale(self.sky,(360,self.game.DISPLAY_H)))
        self.floor=pygame.surfarray.array3d(pygame.image.load("floor.jpg"))
        self.new_frame()
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
    def new_frame(self):
        for i in range(self.game.HALFVRES):
            self.game.rot_i=self.game.rot+np.deg2rad(i/self.game.mod-30)
            sin,cos,cos2=np.sin(self.game.rot_i),np.cos(self.game.rot_i),np.cos(np.deg2rad(i/self.game.mod-30))
            self.game.frame[i][:self.game.HALFVRES]=self.sky[int(np.rad2deg(self.game.rot_i)%360)][:self.game.HALFVRES]/255
            xs,ys=self.game.posx+self.game.ns*cos/cos2,self.game.posy+self.game.ns*sin/cos2 
            xxs,yys=(xs/2%1*99).astype("int"),(ys/2%1*99).astype("int")
            self.game.frame[i][2*self.game.HALFVRES-len(self.game.ns):2*self.game.HALFVRES]=self.game.shade*self.floor[np.flip(xxs),np.flip(yys)]/255
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