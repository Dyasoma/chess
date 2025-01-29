import sys
import pygame
from random import randint
from pygame.locals import *
from chess.constants import WINDOWWIDTH, WINDOWHEIGHT, BOARDSIDELENGTH, SQUARECOUNT, DARKRED, LIGHTBROWN, WHITE, BLACK, SQUARESIZE
from chess.board import Board
from chess.piece import Piece
# from chess.square import Square
# from chess.piece import Pawn
FPS = 1


def main():
    WINDOWSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption("Chess")
    WINDOWSURF.fill("Grey")
    chessboard = Board(BOARDSIDELENGTH, BOARDSIDELENGTH, SQUARECOUNT, DARKRED, LIGHTBROWN)
    piece = Piece(BLACK, 5, 2, "queen") # get piece
    piece_1 = Piece(WHITE, 5, 2, "queen")

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
        chessboard.move_piece(piece, randint(0, 7), randint(0, 7)) 
        chessboard.move_piece(piece_1, randint(0, 7), randint(0, 7))
        # RENDER
            
        chessboard.draw_pieces()
        chessboard.draw_board(WINDOWSURF)

        #draw piece onto board
        pygame.display.update()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
