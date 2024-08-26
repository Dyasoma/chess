import sys
import pygame
from pygame.locals import *
from chess.constants import WINDOWWIDTH, WINDOWHEIGHT
from chess.board import Board
from chess.square import Square
from chess.piece import Pawn


FPS = 60


def main():
    screen = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption("Chess")
    screen.fill("White")

    # Setup and Initialization
    pygame.init()
    game_is_running = True
    clock = pygame.time.Clock()
    # Chess pieces

    while game_is_running:

        # poll for events
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        # UPDATE

        # RENDER
        pygame.display.update()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
