import pygame
import sys
from random import randint
from objects.constants import (
    WINDOWWIDTH,
    WINDOWHEIGHT,
    SQUARESIZE,
    SQUARECOUNT,
    DARKCOLOR,
    LIGHTCOLOR,
    WHITEPLAYER,
    BLACKPLAYER,
    BLACK,
    WHITE,
    GREY,
)


from objects.board import GameBoard
from objects.game_state import GameState
from objects.team import Team


FPS = 60

# TODO:
# Add move tracking. i.e. after move print something like p moves to e7 or queen takes black pawn at e5
#
def setup():
    pygame.init()
    window = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption("Chess")  # window title
    window.fill(GREY)
    chessboard = GameBoard(
        SQUARESIZE, SQUARECOUNT, DARKCOLOR, LIGHTCOLOR, window
    )  # create a board
    chessboard.draw_board()
    pygame.display.update()
    black_player = Team(BLACKPLAYER, BLACK)
    white_player = Team(WHITEPLAYER, WHITE)
    chessboard.set_pieces(black_player.active_pieces, white_player.active_pieces)
    return (True, pygame.time.Clock(), chessboard, black_player, white_player)


def main():
    # Setup and Initialization
    delta_report = 0
    game_is_running, clock, chessboard, black_player, white_player = setup()
    game_state = GameState(chessboard, black_player, white_player)
    while game_is_running:
        if black_player.get_count_active() == 0 or white_player.get_count_active() == 0:
            game_is_running = False
            break
        game_state.handle_events()
        game_state.update_state()
        game_state.render()
        delta_report += 1
        clock.tick(FPS)
        """        
        if delta_report == 50:
            print("\n"*2)
            print(f"Current Player : {game_state.print_current_player()}")
            print(f"Black Pieces {black_player.get_count_active()}")
            print(f"Captured Black Pieces : {black_player.get_count_captured()}")
            print(f"White Pieces {white_player.get_count_active()}")
            print(f"Captured White Pieces : {white_player.get_count_captured()}")
            print("\n"*2)
            delta_report = 0
        """

        pygame.display.update()
    pygame.quit()


if __name__ == "__main__":
    main()
