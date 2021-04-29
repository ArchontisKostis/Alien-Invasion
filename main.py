# Main Program For ALIEN INVASION Game by Archontis Kostis.
# All Rights Reserved. Code-Development --> Archontis Kostis  Sound Effects & Music --> Stavros Mavroudis
# VERSION: Beta v2.1.0

# -------- WHAT IS NEW --------
# 05/03/2021 --> Development BETA v1.0.0

# 06/03/2021 --> Main Menu Added (BETA v1.2.0)
# 06/03/2021 --> Added ---> Options Menu, Credits Menu (BETA v2.0.0)

# 07/03/2021 --> Added Music ON/OFF & Sound ON/OFF in Options Menu (BETA v2.1.0)
# 07/03/2021 --> Added Exit Button in Main Menu (BETA v2.1.2)

# 08/03/2021 --> Main Menu Background Design and Add it to Code

# -------- TO DO --------
# Create Help Menu --> Controls Hint
# Options Menu --> Change Controls (Arrows OR wsda)

from game import *

g = Game()
player = Player()
bullet = Bullet()
enemy = Enemy()

def play_music():
    # BG Music
    mixer.music.load('files/sounds/background.wav')
    mixer.music.play(-1)

# MAIN PROGRAM
play_music()
while g.running:
    g.curr_menu.display_menu()
    g.game_loop( bullet, enemy)

    
