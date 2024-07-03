
# Example file showing a basic pygame "game loop"
import pygame, sys
from pygame.locals import *
WINDOWWIDTH = 800
WINDOWHEIGHT = 800
FPS = 30

screen = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
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
    
    #UPDATE

    # RENDER
    pygame.display.update()
    FPSCLOCK.tick(FPS)
    
pygame.quit()