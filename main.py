
import pygame
from random import randint
from objects.constants import (
    WINDOWWIDTH,
    WINDOWHEIGHT,
    BOARDSIDELENGTH,
    SQUARECOUNT,
    DARKRED,
    LIGHTBROWN, 
    GREEN,
    BOARDPOSX,
    BOARDPOSY,
)


from objects.board import Board
from objects.game_state import GameState

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


def render(chessboard : Board, WINDOWSURF : pygame.Surface):
    chessboard.draw_board()  # draw board onto the window
    chessboard.draw_highlights(GREEN, WINDOWSURF)
    WINDOWSURF.blit(chessboard.surface, (BOARDPOSX, BOARDPOSY))
    chessboard.draw_pieces(WINDOWSURF)  # draw all pieces onto the board
    WINDOWSURF.blit(chessboard.highlighted_surface, (BOARDPOSX, BOARDPOSY))

def main():
    # Setup and Initialization
    game_is_running, clock, WINDOWSURF, chessboard, black_pieces, white_pieces = setup()
    game_state = GameState(chessboard)
    while game_is_running:

        game_state.handle_events()

        game_state.update_logic()

        render(chessboard, WINDOWSURF)
        
        clock.tick(FPS)

        pygame.display.update()
    pygame.quit()


if __name__ == "__main__":
    main()
