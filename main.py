import sys
import pygame
from random import randint
from pygame.locals import *
from objects.constants import WINDOWWIDTH, WINDOWHEIGHT, BOARDSIDELENGTH, SQUARECOUNT, DARKRED, LIGHTBROWN, WHITE, BLACK, SQUARESIZE, GREEN
from objects.board import Board

FPS = 60


def setup():
    pygame.init()
    window = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption("Chess") # window title
    window.fill("Grey")
    chessboard = Board(BOARDSIDELENGTH, BOARDSIDELENGTH, SQUARECOUNT, DARKRED, LIGHTBROWN) # create a board
    black_pieces = []
    white_pieces = []
    chessboard.load_pieces(black_pieces, white_pieces)
    return (True, pygame.time.Clock(), window, chessboard, black_pieces, white_pieces)


def main():
    # Setup and Initialization
    game_is_running, clock, WINDOWSURF, chessboard, black_pieces, white_pieces = setup() 
    row, col = (None, None)
    mouse_pressed = False
    piece = None
    state = 0
    valid_moves = None
    debug_next = False
    draw_valid_moves = False
    clear_valid_moves = False
    while game_is_running:
    # main game loop
        # Get Input
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                # get the mouse position
                mouse_pressed = True
                

        # UPDATE
        if state == 0: # select piece phase
            if mouse_pressed: # mouse is pressed
                row, col = chessboard.mouse_pos_to_grid(pygame.mouse.get_pos())
                piece = chessboard.get_piece(row, col)
                if (row, col) != (None, None): # actual piece is located there
                    # select a piece
                    valid_moves = piece.generate_valid_moves(chessboard)
                    # move to next state
                    state = 1 # go to move selection
                    row,col = None, None
            mouse_pressed = False # clear mouse_pressed
        elif state == 1:
            draw_valid_moves = True
            if not valid_moves or len(valid_moves) == 0:
                state = 0
                draw_valid_moves = False
            elif (row, col) == (piece.row, piece.col):
                state = 0
                draw_valid_moves = False
                clear_valid_moves = True
            else:
                if mouse_pressed:
                    row, col = chessboard.mouse_pos_to_grid(pygame.mouse.get_pos())
                    if (row, col) != (None, None):
                        if (row, col) in valid_moves:
                            # move the piece
                            chessboard.move_piece(piece, row, col)
                            state = 0
                            clear_valid_moves = True
                        else:
                            state = 0
                            draw_valid_moves = False
                            clear_valid_moves = True
            mouse_pressed = False



        # RENDER
        if draw_valid_moves:
            chessboard.draw_valid_moves(valid_moves)
        if clear_valid_moves:
            chessboard.undraw_moves(valid_moves)
            draw_valid_moves = False
            clear_valid_moves = False
        chessboard.draw_pieces() # draw all pieces onto the board
        chessboard.draw_board(WINDOWSURF) # draw board onto the window

        pygame.display.update()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
