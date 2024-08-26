import sys
import pygame
from pygame.locals import *
from chess.constants import WINDOWWIDTH, WINDOWHEIGHT, BOARDSIDELENGTH, SQUARECOUNT, DARKRED, LIGHTBROWN, WHITE, BLACK
from chess.board import Board
from chess.piece import Piece
# from chess.square import Square
# from chess.piece import Pawn
FPS = 60

start = [5, 3]

def main():
    WINDOWSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption("Chess")
    WINDOWSURF.fill("White")
    chessboard = Board(BOARDSIDELENGTH, BOARDSIDELENGTH, SQUARECOUNT, DARKRED, LIGHTBROWN)
    piece = Piece(WHITE, "pawn") # get piece

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

        #place piece onto structure
        chessboard.struct[start[0]][start[1]].contents = piece
        #draw piece onto board
        chessboard.surface.blit(piece.surface, chessboard.struct[start[0]][start[1]].rel_pos)
        pygame.display.update()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
