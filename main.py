import sys
import pygame
from random import randint
from pygame.locals import *
from objects.constants import (
    WINDOWWIDTH,
    WINDOWHEIGHT,
    BOARDSIDELENGTH,
    SQUARECOUNT,
    DARKRED,
    LIGHTBROWN,
    WHITE,
    BLACK,
    SQUARESIZE,
    GREEN,
)

SELECTPIECE = 0
SELECTMOVE = 1
from objects.board import Board

FPS = 30


def setup():
    pygame.init()
    window = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption("Chess")  # window title
    window.fill("Grey")
    chessboard = Board(
        BOARDSIDELENGTH, BOARDSIDELENGTH, SQUARECOUNT, DARKRED, LIGHTBROWN
    )  # create a board
    black_pieces, white_pieces = chessboard.load_pieces()
    chessboard.set_pieces(black_pieces, white_pieces)
    return (True, pygame.time.Clock(), window, chessboard, black_pieces, white_pieces)


def main():
    # Setup and Initialization
    game_is_running, clock, WINDOWSURF, chessboard, black_pieces, white_pieces = setup()
    row, col = (None, None)
    mouse_pressed = False
    mouse_pos = (None, None)
    selected_piece = None

    state = SELECTPIECE
    legal_moves = None
    draw_legal_moves = False
    clear_legal_moves = False

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
                mouse_pos = pygame.mouse.get_pos()

        """
        def handle_piece_selection():
            ...

        def handle_move_selection():
            ...
        if state == SELECTPIECE:
            handle_piece_selection()
        elif state == SELECTMOVE:
            handle_move_selection()

        """
        # UPDATE
        if state == SELECTPIECE:  # select piece phase
            # state conditionals
            if mouse_pressed and chessboard.valid_piece_selected(
                mouse_pos
            ):  # mouse is pressed
                # update state variable
                row, col = chessboard.mouse_pos_to_grid(mouse_pos)
                selected_piece = chessboard.get_piece(row, col)
                legal_moves = chessboard.generate_legal_moves(selected_piece)
                draw_legal_moves = True
                state = 1  # go to move selection
                # sanitize
                mouse_pressed = False
        elif state == SELECTMOVE:
            # state conditionals
            if not legal_moves:
                # update state variables
                state = 0
                clear_legal_moves = True
            elif mouse_pressed and chessboard.valid_move_selected(
                mouse_pos, legal_moves
            ):
                # update state variables
                row, col = chessboard.mouse_pos_to_grid(mouse_pos)
                # move the piece
                chessboard.move_piece(selected_piece, row, col)
                state = 0
                clear_legal_moves = True
                # sanitize
            elif mouse_pressed and (chessboard.mouse_pos_to_grid(mouse_pos)) == (
                selected_piece.row,
                selected_piece.col,
            ):
                state = 0
                clear_legal_moves = True
        mouse_pressed = False

        # RENDER
        if draw_legal_moves:
            chessboard.draw_legal_moves(legal_moves)
            draw_legal_moves = False
        elif clear_legal_moves:
            chessboard.undraw_moves(legal_moves)
            clear_legal_moves = False
            # we have the highlighted surface now

        chessboard.draw_pieces()  # draw all pieces onto the board
        chessboard.draw_board(WINDOWSURF)  # draw board onto the window

        pygame.display.update()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
