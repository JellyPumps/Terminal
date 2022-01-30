import pygame
#---
class Menu():
    def __init__(self,game):
        self.game=game
        self.mid_w,self.mid_h=self.game.DISPLAY_W/2,self.game.DISPLAY_H/2
        self.run_display=True
        self.cursor_rect=pygame.Rect(0,0,20,20)
        self.offset=-100
    def draw_cursor(self):
        self.game.draw_text(">",15,self.cursor_rect.x,self.cursor_rect.y)
    def blit_screen(self):
        self.game.window.blit(self.game.display,(0,0))
        pygame.display.update()
        self.game.reset_key()
class MainMenu(Menu):
    def __init__(self,game):
        Menu.__init__(self,game)
        self.state="Start"
        self.startx,self.starty=self.mid_w-250,(self.mid_h-280)+30
        self.optionsx,self.optionsy=self.mid_w-250,(self.mid_h-280)+50
        self.creditsx,self.creditsy=self.mid_w-250,(self.mid_h-280)+70
        self.cursor_rect.midtop=(self.startx+self.offset,self.starty)
    def display_menu(self):
        self.run_display=True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill(self.game.BLACK)
            self.game.draw_text("root@host:~$ ./terminal",20,self.game.DISPLAY_W/2-250,self.game.DISPLAY_H/2-280)
            self.game.draw_text("Start",20,self.startx,self.starty)
            self.game.draw_text("Options",20,self.optionsx,self.optionsy)
            self.game.draw_text("Credits",20,self.creditsx,self.creditsy)
            self.draw_cursor()
            self.blit_screen()
    def move_cursor(self):
        if self.game.K_DOWN:
            if self.state=="Start":
                self.cursor_rect.midtop=(self.optionsx+self.offset,self.optionsy)
                self.state="Options"
            elif self.state=="Options":
                self.cursor_rect.midtop=(self.creditsx+self.offset,self.creditsy)
                self.state="Credits"
            elif self.state=="Credits":
                self.cursor_rect.midtop=(self.startx+self.offset,self.starty)
                self.state="Start"
        elif self.game.K_UP:
            if self.state=="Start":
                self.cursor_rect.midtop=(self.creditsx+self.offset,self.creditsy)
                self.state="Credits"
            elif self.state=="Options":
                self.cursor_rect.midtop=(self.startx+self.offset,self.starty)
                self.state="Start"
            elif self.state=="Credits":
                self.cursor_rect.midtop=(self.optionsx+self.offset,self.optionsy)
                self.state="Options"
    def check_input(self):
        self.move_cursor()
        if self.game.K_START:
            if self.state=="Start":
                self.game.playing=True
            elif self.state=="Options":
                self.game.curr_menu=self.game.options
            elif self.state=="Credits":
                self.game.curr_menu=self.game.credits
            self.run_display=False
class Options(Menu):
    def __init__(self,game):
        Menu.__init__(self,game)
        self.state="Volume"
        self.volx,self.voly=self.mid_w-250,(self.mid_h-280)+30
        self.controlsx,self.controlsy=self.mid_w-250,(self.mid_h-280)+50
        self.cursor_rect.midtop=(self.volx+self.offset,self.voly)
    def display_menu(self):
        self.run_display=True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill(self.game.BLACK)
            self.game.draw_text("admin@admin:~$ ./terminal --options",20,self.game.DISPLAY_W/2-250,self.game.DISPLAY_H/2-280)
            self.game.draw_text("Volume",20,self.volx,self.voly)
            self.game.draw_text("Controls",20,self.controlsx,self.controlsy)
            self.draw_cursor()
            self.blit_screen()
    def check_input(self):
        if self.game.K_BACK:
            self.game.curr_menu=self.game.main_menu
            self.run_display=False
        elif self.game.K_UP or self.game.K_DOWN:
            if self.state=="Volume":
                self.state="Controls"
                self.cursor_rect.midtop=(self.controlsx+self.offset,self.controlsy)
            elif self.state=="Controls":
                self.state="Volume"
                self.cursor_rect.midtop=(self.volx+self.offset,self.voly)
        elif self.game.K_START:
            #TODO
            pass
class Credits(Menu):
    def __init__(self,game):
        Menu.__init__(self,game)
    def display_menu(self):
        self.run_display=True
        while self.run_display:
            self.game.check_events()
            if self.game.K_BACK or self.game.K_START:
                self.game.curr_menu=self.game.main_menu
                self.run_display=False
            self.game.display.fill(self.game.BLACK)
            self.game.draw_text("admin@admin:~$ ./terminal --credits",20,self.game.DISPLAY_W/2-250,self.game.DISPLAY_H/2-280)
            self.game.draw_text("Made By: SMVBJ // JellyP",20,self.mid_w-250,(self.mid_h-280)+30)
            self.blit_screen()
            
                