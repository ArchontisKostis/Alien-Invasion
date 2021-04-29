import pygame
from tkinter import messagebox
import tkinter as tk

root = tk.Tk()
root.withdraw()

class Menu():
    def __init__(self, game):
        self.game = game

        self.mid_w, self.mid_h = self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2    # Initialize Middle Width - Height
        self.run_display = True
        self.cursor_rect = pygame.Rect(0, 0, 20, 20)    # (x position, y position, width, height)
        self.offset = -100                              # Offset Position

    def draw_cursor(self):
        self.game.draw_text('>', 25, self.cursor_rect.x, self.cursor_rect.y)

    def blit_screen(self):
        self.game.window.blit(self.game.display, (0,0))
        pygame.display.update()
        self.game.reset_key()

class MainMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        # Variables
        self.State = "Start"
        self.startx, self.starty = self.mid_w, self.mid_h + 120      # Start Option Coordinates
        self.optionsx, self.optionsy = self.mid_w, self.mid_h + 150  # Options Option Coordinates
        self.creditsx, self.creditsy = self.mid_w, self.mid_h + 180  # Credits Option Coordinates
        self.exitx, self.exity = self.mid_w, self.mid_h + 265
        self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
        self.play = False
        

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            # Check For Events
            self.game.check_events()
            self.check_input()

            self.game.display.blit(self.game.bg, (0,0))
            # Draw Start Game Text
            self.game.draw_text('Start Game', 25, self.startx, self.starty)
            # Draw Options Text
            self.game.draw_text('Options', 25, self.optionsx, self.optionsy)
            # Draw Credits Text
            self.game.draw_text('Credits', 25, self.creditsx, self.creditsy)
            # Draw Exit Text
            self.game.draw_text('Exit', 20, self.exitx, self.exity)

            # Draw Cursor
            self.draw_cursor()
            self.blit_screen()

    def move_cursor(self):
        # If Player Click Down Key
        if self.game.DOWN_KEY:
            if self.State == 'Start':
                self.cursor_rect.midtop = (self.optionsx + self.offset, self.optionsy)
                self.State = 'Options'

            elif self.State == 'Options':
                self.cursor_rect.midtop = (self.creditsx + self.offset, self.creditsy)
                self.State = 'Credits'

            elif self.State == 'Credits':
                self.cursor_rect.midtop = (self.exitx + self.offset, self.exity)
                self.State = 'Exit'
            
            elif self.State == 'Exit':
                self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
                self.State = 'Start'
        
        # If Player Click Up Key
        elif self.game.UP_KEY:
            if self.State == 'Start':
                self.cursor_rect.midtop = (self.exitx + self.offset, self.exity)
                self.State = 'Exit'

            elif self.State == 'Options':
                self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
                self.State = 'Start'

            elif self.State == 'Credits':
                self.cursor_rect.midtop = (self.optionsx + self.offset, self.optionsy)
                self.State = 'Options'

            elif self.State == 'Exit':
                self.cursor_rect.midtop = (self.creditsx + self.offset, self.creditsy)
                self.State = 'Credits'

    def check_input(self):
        self.move_cursor()

        if self.game.START_KEY:
            if self.State == 'Start':
                self.game.playing = True
            elif self.State == 'Options':
                self.game.curr_menu = self.game.options
            elif self.State == 'Credits':
                self.game.curr_menu = self.game.credits
            elif self.State == 'Exit':
                ms = messagebox.askquestion("Exit Game?", "Are you sure you want to Exit?", icon = 'warning')
                if ms == 'yes':
                    self.game.running = False
            self.run_display = False


class OptionsMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)

        self.State = 'Volume'
        self.volx, self.voly = self.mid_w, self.mid_h + 120
        self.soundsx, self.soundsy = self.mid_w, self.mid_h + 150
        self.cursor_rect.midtop = (self.volx + self.offset, self.voly)
        self.musicOn = True
        self.opbg = pygame.image.load("files/img/backgrounds/options.png")
        
    
    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()

            self.game.display.blit(self.opbg, (0,0))

            # Draw Options Text (HEADER)
            #self.game.draw_text('OPTIONS', 30, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 + 60)

            # Draw Music ON/OFF Text
            if self.game.music:
                self.game.draw_text('Music ON', 25, self.volx, self.voly)
            else:
                self.game.draw_text('Music OFF', 25, self.volx, self.voly)

            # Draw Sound ON/OFF Text
            if self.game.soundfx:
                self.game.draw_text('Sound ON', 25, self.soundsx, self.soundsy)
            else:
                self.game.draw_text('Sound OFF', 25, self.soundsx, self.soundsy)
                
            # Draw Controls Text
            #self.game.draw_text('Controls', 20, self.controlsx, self.controlsy)

            # Draw
            self.draw_cursor()
            self.blit_screen()
            pygame.display.update()
    
    def check_input(self):
        if self.game.BACK_KEY:      # If User pressed <-- Go back to main menu
            self.game.curr_menu = self.game.main_menu
            self.run_display = False

        elif self.game.UP_KEY: #or self.game.DOWN_KEY:
            if self.State == 'Volume':
                self.State = 'Sound'
                self.cursor_rect.midtop = (self.soundsx + self.offset, self.soundsy)
            elif self.State == 'Sound':
                self.State = 'Volume'
                self.cursor_rect.midtop = (self.volx + self.offset, self.voly)
            #elif self.State == 'Controls':
                #self.State = 'Sound'
                #self.cursor_rect.midtop = (self.soundsx + self.offset, self.soundsy)

        elif self.game.DOWN_KEY: 
            if self.State == 'Volume':
                self.State = 'Sound'
                self.cursor_rect.midtop = (self.soundsx + self.offset, self.soundsy)
            elif self.State == 'Sound':
                self.State = 'Volume'
                self.cursor_rect.midtop = (self.volx + self.offset, self.voly)
            #elif self.State == 'Controls':
            #    self.State = 'Volume'
            #    self.cursor_rect.midtop = (self.volx + self.offset, self.voly)

        elif self.game.START_KEY:
            # TO-DO : Create a Volume Menu and Controls Menu
            if self.State == 'Volume':
                if self.game.music == True:
                    self.game.music = False
                else:
                    self.game.music = True
            
            if self.State == 'Sound':
                if self.game.soundfx == True:
                    self.game.soundfx = False
                else:
                    self.game.soundfx = True

# CREDITS MENU
class CreditsMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.crbg = pygame.image.load("files/img/backgrounds/credits.png")

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()

            if self.game.START_KEY or self.game.BACK_KEY:   # If Player Press Backspace or Enter Go Back to MAIN MENU
                 self.game.curr_menu = self.game.main_menu
                 self.run_display = False
            self.game.display.blit(self.crbg, (0,0))
            self.blit_screen()