
# Example file showing a basic pygame "game loop"
import pygame
WINDOWHEIGHT = 1080
WINDOWWIDTH = 720
# Setup and Initialization
pygame.init()
game_window = pygame.display.set_mode((WINDOWHEIGHT, WINDOWWIDTH))
clock = pygame.time.Clock()
game_is_running = True

while game_is_running:
    
    # Inputs


    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_is_running = False
    

    #UPDATE



    # fill the screen with a color to wipe away anything from last frame
    game_window.fill("purple")


    # RENDER
    # RENDER YOUR GAME HERE
    # flip() the display to put your work on screen
    pygame.display.flip()

    #



    clock.tick(60)  # limits FPS to 60

pygame.quit()