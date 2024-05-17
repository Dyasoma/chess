
# Example file showing a basic pygame "game loop"
import pygame, sys
from pygame.locals import *
import math
WINDOWWIDTH = 750
WINDOWHEIGHT = 500
FPS = 30



DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.display.set_caption("Chess")



# Setup and Initialization
pygame.init()
game_is_running = True
FPSCLOCK = pygame.time.Clock()
#Chess pieces

while game_is_running:
    
    # Inputs
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    
    pygame.display.update()
    FPSCLOCK.tick(FPS)
    #UPDATE
    # fill the screen with a color to wipe away anything from last frame
    # RENDER
    # RENDER YOUR GAME HERE
    # flip() the display to put your work on screen
pygame.quit()