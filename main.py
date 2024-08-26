import sys
import pygame
from pygame.locals import *
from chess.constants import WINDOWWIDTH, WINDOWHEIGHT, BOARDSIDELENGTH, SQUARECOUNT, DARKRED, LIGHTBROWN
from chess.board import Board
# from chess.square import Square
# from chess.piece import Pawn
FPS = 60



def main():
    WINDOWSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption("Chess")
    WINDOWSURF.fill("White")
    chessboard = Board(BOARDSIDELENGTH, BOARDSIDELENGTH, SQUARECOUNT, DARKRED, LIGHTBROWN)

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
        chessboard.draw_board(WINDOWSURF)
        pygame.display.update()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
