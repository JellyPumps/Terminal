import pygame
import sys
from menu import *
#---
class Game():
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Terminal")
        self.running,self.playing=True,False
        self.K_UP,self.K_DOWN,self.K_START,self.K_BACK=False,False,False,False
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
    class GameState():
        def __init__(self):
            self.state="Level_1"
        def level_1(self):
            pass
    def game_loop(self):
        while self.playing:
            self.check_events()
            self.display.fill(self.BLACK)
            self.draw_text('Placeholder',20,self.DISPLAY_W/2,self.DISPLAY_H/2)
            self.window.blit(self.display,(0,0))
            pygame.display.update()
            self.reset_key()
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
    def reset_key(self):
        self.K_UP,self.K_DOWN,self.K_START,self.K_BACK=False,False,False,False
    def draw_text(self,text,size,x,y):
        font=pygame.font.Font(self.font_name,size)
        text_surface=font.render(text,True,self.WHITE)
        text_rect=text_surface.get_rect()
        text_rect.center=(x,y)
        self.display.blit(text_surface,text_rect)