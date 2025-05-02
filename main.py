import sys
import pygame
from random import randint
from pygame.locals import *
from objects.constants import WINDOWWIDTH, WINDOWHEIGHT, BOARDSIDELENGTH, SQUARECOUNT, DARKRED, LIGHTBROWN, WHITE, BLACK, SQUARESIZE
from objects.board import Board
from objects.piece import Pawn, Knight, Bishop, Rook, Queen, King

FPS = 1

def main():
    # Setup and Initialization
    pygame.init()
    game_is_running = True
    clock = pygame.time.Clock()

    # Setup Game materials
    WINDOWSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT)) # window
    pygame.display.set_caption("Chess") # window title
    WINDOWSURF.fill("Grey") # color of window
    chessboard = Board(BOARDSIDELENGTH, BOARDSIDELENGTH, SQUARECOUNT, DARKRED, LIGHTBROWN) # create a board
    black_pieces = []
    white_pieces = []
    chessboard.load_pieces(black_pieces, white_pieces)
    
    move_value = 0

    # Chess pieces

    while game_is_running:
    # main game loop
        # Get Input
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        # UPDATE
        
        #chessboard.move_piece(piece, piece.row + randint(-7, 7), piece.col+randint(-7,7))

        # RENDER
            
        chessboard.draw_pieces() # draw all pieces onto the board
        chessboard.draw_board(WINDOWSURF) # draw board onto the window

        pygame.display.update()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
