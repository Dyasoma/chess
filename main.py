import pygame
from random import randint
from objects.constants import (
    WINDOWWIDTH,
    WINDOWHEIGHT,
    BOARDSIDELENGTH,
    SQUARECOUNT,
    DARKCOLOR,
    LIGHTCOLOR, 
    WHITEPLAYER,
    BLACKPLAYER,
    BLACK,
    WHITE,
    GREY
)


from objects.board import Board
from objects.game_state import GameState
from objects.team import Team

FPS = 60


def setup():
    pygame.init()
    window = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption("Chess")  # window title
    window.fill(GREY)
    chessboard = Board(
        BOARDSIDELENGTH, BOARDSIDELENGTH, SQUARECOUNT, DARKCOLOR, LIGHTCOLOR
    )  # create a board
    ## CHANGED FOR TESTING.
    black_player = Team(BLACKPLAYER, BLACK) 
    white_player = Team(WHITEPLAYER, WHITE)
    chessboard.set_pieces(black_player.active_pieces, white_player.active_pieces)
    return (True, pygame.time.Clock(), window, chessboard, black_player, white_player)


def main():
    # Setup and Initialization
    delta_report = 0
    game_is_running, clock, WINDOWSURF, chessboard, black_player, white_player = setup()
    game_state = GameState(chessboard, black_player, white_player)
    while game_is_running:
        if black_player.get_active_pieces() == 0 or white_player.get_active_pieces() == 0:
            game_is_running = False
            break
        game_state.handle_events()

        game_state.update_logic()

        game_state.render(WINDOWSURF)
        delta_report += 1
        clock.tick(FPS)
        if delta_report == 50:
            print("\n"*2)
            print(f"Current Player : {game_state.print_current_player()}")
            print(f"Black Pieces {black_player.get_active_pieces()}")
            print(f"Captured Black Pieces : {black_player.get_captured_pieces()}")
            print(f"White Pieces {white_player.get_active_pieces()}")
            print(f"Captured White Pieces : {white_player.get_captured_pieces()}")
            print("\n"*2)
            delta_report = 0



        pygame.display.update()
    pygame.quit()


if __name__ == "__main__":
    main()
