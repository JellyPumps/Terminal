import pygame
import sys
import math
import numpy as np
import time
from menu import *
from gamestate import *
#---
#Removed GameState(), moved gamestate.py
#---
class Game():
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Terminal")
        self.clock=pygame.time.Clock()
        self.running,self.playing=True,False
        self.K_UP,self.K_DOWN,self.K_START,self.K_BACK,self.K_E=False,False,False,False,False
        self.K_LEFT,self.K_RIGHT=False,False
        self.DISPLAY_W,self.DISPLAY_H=800,600
        self.display=pygame.Surface((self.DISPLAY_W,self.DISPLAY_H))
        self.window=pygame.display.set_mode(((self.DISPLAY_W,self.DISPLAY_H)))
        self.font_name='VCR_OSD_MONO_1.001.ttf'
        self.BLACK,self.WHITE=(0,0,0),(255,255,255)
        #Menu
        self.main_menu=MainMenu(self)
        self.options=Options(self)
        self.credits=Credits(self)
        self.curr_menu=self.main_menu
        #CAMERAAAA
        self.HALFVRES=300
        self.mod=self.DISPLAY_W/60 #Scaling factor(60 deg fov)
        self.posx,self.posy,self.rot=0,0,0
        self.frame=np.ones([self.DISPLAY_W,self.DISPLAY_H,3])
        self.ns=self.HALFVRES/((self.HALFVRES+0.1-np.linspace(0,self.HALFVRES,self.HALFVRES)))#depth
        self.cos22=np.cos(np.deg2rad(np.linspace(-30,-30,self.DISPLAY_W)/self.mod))#perspective correction
        self.shade=0.4+0.6*(np.linspace(0,self.HALFVRES,self.HALFVRES)/self.HALFVRES)
        self.shade=np.dstack((self.shade,self.shade,self.shade))
        #---
        self.game_state=GameState(self)
        #---
        self.last_time=time.time()
    #
    #Removed Vision loop and Movement, moved to gamestate.py
    #
    def game_loop(self):
        while self.playing:
            self.clock.tick(30)
            self.fps=int(self.clock.get_fps())
            pygame.display.set_caption("Terminal - FPS: "+str(self.fps))
            self.check_events()
            #----
            self.display.fill(self.BLACK)
            #----
            #self.draw_text('Placeholder',20,self.DISPLAY_W/2,self.DISPLAY_H/2)
            self.game_state.state_manager()
            self.window.blit(self.display,(0,0)) 
            self.posx,self.posy,self.rot=self.game_state.movement(self.posx,self.posy,self.rot,pygame.key.get_pressed(),self.clock.tick()/200)
            pygame.display.update()
    def check_events(self):
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                self.running,self.playing=False,False
                self.curr_menu.run_display=False
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_RETURN:
                    self.K_START=True
                if event.key==pygame.K_BACKSPACE:
                    self.K_BACK=True
                if event.key==pygame.K_DOWN:
                    self.K_DOWN=True               
                if event.key==pygame.K_UP:
                    self.K_UP=True
                if event.key==pygame.K_e:
                    self.K_E=True
    def reset_key(self):
        self.K_UP,self.K_DOWN,self.K_START,self.K_BACK=False,False,False,False
    def draw_text(self,text,size,x,y):
        font=pygame.font.Font(self.font_name,size)
        text_surface=font.render(text,True,self.WHITE)
        text_rect=text_surface.get_rect()
        text_rect.center=(x,y)
        self.display.blit(text_surface,text_rect)