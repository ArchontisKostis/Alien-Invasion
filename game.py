# Libraries
import pygame
import random
import math
from menu import *

from pygame import mixer


                    

# ------------------------------------------------------------------------------------------------------------------------------------------ #

# Player Class
class Player():
    def __init__(self):
        # Player
        self.playerImg = pygame.image.load("files/img/items/jet.png")      # Initialize Player Img
        self.playerX = 370   # X position
        self.playerY = 480   # Y position
        self.playerX_change = 0

    # PLAYER Draw Function
    def playerDraw(self):
        self.window.blit(self.playerImg, (self.playerX, self.playerY))      # Draw Player (player, (coordinates))
    
    # Function that stops player from Exiting the window Boundary
    def boundary(self):
        # Code for Boundary
        if self.playerX <= 0:
            self.playerX = 0
        elif self.playerX >= 736:    # Επειδη το μεγεθος της εικονας player θελουμε να σταματαει μολις η ακρη του φτασει στο οριο της οθονης
            self.playerX = 736       # Αφαιρουμε το Width της εικονας απο το οριο της οθονης ωστε να σταματησει ακριβως στην ακρη της εικονας (εκχωριση τιμης στην συντεταγμενη Χ του Παικτη)               

# Enemy Class
class Enemy():
    def __init__(self):
        # Enemy
        self.enemyImg = []
        self.enemyX = []
        self.enemyY = []
        self.enemyX_change = []
        self.enemyY_change = []
        self.numEnemies = 6

        # Store Enemies in List
        for i in range(self.numEnemies):
            self.enemyImg.append(pygame.image.load("files/img/items/enemy.png"))      # Initialize Enemy Img
            self.enemyX.append(random.randint(0, 735))                    # X position (Use Random Module on Enemy to appear in random position)
            self.enemyY.append(random.randint(50, 150))                   # Y position (Use Random Module on Enemy to appear in random position)
            self.enemyX_change.append(2)
            self.enemyY_change.append(40)
    
    # ENEMY Draw Function
    def enemyDraw(self, i):
        self.window.blit(self.enemyImg[i], (self.enemyX[i], self.enemyY[i]))      # Draw Enemy (enemy, (coordinates))

# Bullet Class
class Bullet():
    def __init__(self):
        # Bullet
        self.bulletImg = pygame.image.load("files/img/items/bullet.png")
        self.bulletX = 0      # X position (Use Random Module on Enemy to appear in random position)
        self.bulletY = 480    # Y position (Use Random Module on Enemy to appear in random position)
        self.bulletX_change = 0
        self.bulletY_change = 5
        self.bulletState = "ready"   # Ready -> You can't see the bullet  Fire -> The Bullet is moving

    # Function to Fire Bullet
    def fire_bullet(self):
        self.bulletState = "fire"
        self.window.blit(self.bulletImg, (self.bulletX+16, self.bulletY+10))




class Game(Player, Enemy, Bullet):
    def __init__(self):
        Player.__init__(self)
        Enemy.__init__(self)
        Bullet.__init__(self)

        pygame.init()   # PyGame initialization
        # Data Initialization
        self.running, self.playing = True, False    
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY = False, False, False, False
        self.DISPLAY_W, self.DISPLAY_H = 800, 600   # Canvas Size
        self.distance = 100
        self.music, self.soundfx = False, True

        # Make Canvas
        self.display = pygame.Surface((self.DISPLAY_W, self.DISPLAY_H))
        self.window  = pygame.display.set_mode((self.DISPLAY_W, self.DISPLAY_H))

        self.font_name = "font1.ttf"      # Font Name Initialization

        self.Black, self.White = (0,0,0), (255,255,255)     # Black and White RGB code Initialization

        # Background
        self.background = pygame.image.load("files/img/backgrounds/bg2.png")

        # Title and Icon
        pygame.display.set_caption("Alien Invasion BETA")     # Change Window Title

        icon = pygame.image.load("files/img/icon.png")       # Initialize Icon img
        pygame.display.set_icon(icon)                        # Change Icon

        ## Background
        self.bg = pygame.image.load("files/img/backgrounds/mainmenu.png")

        # Score
        self.score_value = 0
        self.score = 0
        self.font = pygame.font.Font('files/fonts/ka1.ttf', 20)
        self.textX = 10
        self.textY = 15

        # Game Over Text
        self.overFont = pygame.font.Font('files/fonts/ka1.ttf', 50)

        # Menus
        self.main_menu = MainMenu(self)
        self.options = OptionsMenu(self)
        self.credits = CreditsMenu(self)
        self.curr_menu = self.main_menu

    # Game Loop Function
    def game_loop(self, Bullet, Enemy):
        while self.playing:
            self.check_events()     # Call Function to Check Events

            if self.BACK_KEY:
                self.reset_game()
                break
            else:
                
                # Create Canvas with Background
                self.window.blit(self.background, (0,0))

                # Move player
                self.playerX += self.playerX_change
                # Check Boundary for Player
                self.boundary()

                # Enemy Movement
                for i in range(self.numEnemies):
                    self.enemyX[i] += self.enemyX_change[i]

                    # Game Over
                    if self.enemyY[i] > 440:    #440
                        for j in range(self.numEnemies):
                            self.enemyY[j] = 2000
                        self.gameOver()
                        

                    # Check if Enemy Hit Boundaries
                    if self.enemyX[i]<=0:
                        self.enemyX_change[i] = 2
                        self.enemyY[i] += self.enemyY_change[i]
                    elif self.enemyX[i] >= 736:
                        self.enemyX_change[i] = -2
                        self.enemyY[i] += self.enemyY_change[i]

                    # Collision Detection
                    collision = self.isCollision(i)
                    if collision:
                        self.explosion = mixer.Sound("files/sounds/explosion.wav")
                        if self.soundfx:
                            self.explosion.play()
                        self.bulletY = 480
                        self.bulletState = "ready"
                        self.score_value += 1
                        self.score += 1

                        self.enemyX[i] = random.randint(0, 735)     # X position (Use Random Module on Enemy to appear in random position)
                        self.enemyY[i] = random.randint(50, 150)    # Y position (Use Random Module on Enemy to appear in random position)
                
                    self.enemyDraw(i)

                # Bullet Movement
                if self.bulletY <= 0:            # If Bullet Reach end of window
                    self.bulletY = 480           # Reset bullet position
                    self.bulletState = "ready"   # Reset Bullet State
                if self.bulletState == "fire":
                    self.fire_bullet()
                    self.bulletY -= self.bulletY_change
                
                self.playerDraw()
                self.showScore()
                pygame.display.update()
                self.reset_key()

    # Event Handler Function
    def check_events(self):
        for event in pygame.event.get():
            if self.music == False:
               mixer.music.pause()
            else:
                mixer.music.unpause()

            if event.type == pygame.QUIT:
                self.running, self.playing = False, False
                self.curr_menu.run_display = False
            
            if event.type == pygame.KEYDOWN:    # If Player Presses a Key on Keyboard
                # if Enter is Pressed
                if event.key == pygame.K_RETURN:    
                    self.START_KEY = True
                # if Backspace is Pressed
                if event.key == pygame.K_BACKSPACE:
                    self.BACK_KEY = True
                # if Down Key is Pressed
                if event.key == pygame.K_DOWN:
                    self.DOWN_KEY = True
                # if Up Key is Pressed
                if event.key == pygame.K_UP:
                    self.UP_KEY = True

                if event.key == pygame.K_LEFT:
                    self.playerX_change = -3
                if event.key == pygame.K_RIGHT:
                    self.playerX_change = 3
                
                # Fire
                if event.key == pygame.K_SPACE:
                    if self.bulletState == "ready":
                        self.bulletSound = mixer.Sound("files/sounds/laser.wav")
                        if self.soundfx:
                            self.bulletSound.play()
                        # Get Current X Coordinate of Spaceship
                        self.bulletX = self.playerX
                        self.fire_bullet()
                
            # If player relaeases key
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                   self.playerX_change = 0     
            
    # Key Reset Function
    def reset_key(self):
        self.START_KEY, self.BACK_KEY, self.DOWN_KEY, self.UP_KEY = False, False, False, False

    # Draw Text Function
    def draw_text(self, text, size, x,y):
        font = pygame.font.Font(self.font_name, size)   # Initialize Font
        text_surface = font.render(text, True, self.White)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)

        self.display.blit(text_surface, text_rect)



    # Check if there is a collision
    def isCollision(self, i):
        self.distance = math.sqrt( (math.pow(self.enemyX[i] - self.bulletX, 2)) + (math.pow(self.enemyY[i] - self.bulletY, 2)) )
        # Colision Detection
        if self.distance < 27:
            return True
        else:
            return False

    # Show Score Function
    def showScore(self):
        score = self.font.render( "Score  " + str(self.score_value), True, (255, 255, 255) )
        self.window.blit(score, (self.textX, self.textY))

    # Game Over!
    def gameOver(self):
        scoreTxt = self.font.render( "Score  " + str(self.score), True, (255, 255, 255) )
        self.score_value = 0

        overTxt = self.overFont.render( "GAME OVER", True, (255, 255, 255) )
        self.window.blit(overTxt, (200, 250))
        self.window.blit(scoreTxt, (350, 350))

    def reset_game(self):
        # Reset Game Data
        self.playing = False
        self.score = 0
        self.score_value = 0

        # Reset Enemy Position
        for i in range(self.numEnemies):
            self.enemyY[i] = random.randint(50, 150)
        
        # Reset Player Data
        self.playerX = 370   # X position
        self.playerY = 480   # Y position
        self.playerX_change = 0