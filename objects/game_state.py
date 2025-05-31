from .constants import (
    SELECTPIECE,
    SELECTMOVE,
    SELECTPROMOTION,
    GREEN,
    BLACK,
    WHITE,
)
from .board import Board
from pygame.locals import *
from .piece import Piece
from .promotion_menu import PromotionMenu
from .team import Team
import pygame
import sys


class GameState:
    """
    Over-arching object that controls game state.

    Args:
        board (Board): The chessboard the game will be played on
        dark_team (Team): The Black players team, i.e. collection of their pieces they will play with
        light_team (Team): The White players team, i.e. collection of their pieces they will play with

    Attributes:
        mouse_pressed (Bool): Whether or not the mouse has been pressed, for state functions this value must continuously
        be set to False
        mouse_pos (tuple[int, int]): The mouse position (x, y) relative to the top-left of the game window
        selected_piece (Piece): The current selected piece obtained from mouse selection
        captured_piece (Piece): The last captured piece obtained from piece capturing
        legal_moves (list[tuple[int ,int]]): A list of tuples which represent legal moves
        state (int): The current game state, whether a player is selecting a piece, moving the piece or upgrading a piece.
        board (Board): The chessboard the game will be played on
        dark_team (Team): The Black players team, i.e. collection of their pieces they will play with
        light_team (Team): The White players team, i.e. collection of their pieces they will play with
        current_player (int): The current player whose turn it is
        promotion_menu (PromotionMenu): The object representing the upgrade menu once a pawn reaches the enemy main rank.

    """

    def __init__(self, board: Board, dark_team: Team, light_team: Team):
        self.mouse_pressed = False
        self.mouse_pos: tuple[int, int] = (0, 0)
        self.selected_piece: Piece = None
        self.captured_piece: Piece = None
        self.legal_moves: list[tuple[int, int]] = []
        self.state: int = SELECTPIECE
        self.board: Board = board
        self.dark_team: Team = dark_team
        self.light_team: Team = light_team
        self.current_player: Team = self.light_team
        self.promotion_menu = None

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                self.set_mouse_pressed(True)
                self.set_mouse_pos(*pygame.mouse.get_pos())

    def update_state(self):
        if self.state == SELECTPIECE:
            self.handle_piece_selection()
        elif self.state == SELECTMOVE:
            self.handle_move_selection()
        elif self.state == SELECTPROMOTION:
            self.handle_promotion_selection()

    def handle_piece_selection(self):
        # state conditionals
        if self.mouse_pressed and self.valid_square_selected(self.mouse_pos):
            # convert pos to board values
            row, col = self.board.mouse_pos_to_grid(self.mouse_pos)
            # check if that square has a piece
            self.set_selected_piece(self.board.get_square_contents(row, col))
            ## we now have a piece, check that it is valid for the given player
            if (
                self.selected_piece
                and self.selected_piece.color == self.current_player.color
            ):
                self.set_legal_moves(
                    self.board.generate_legal_moves(self.selected_piece)
                )
                self.board.set_highlighted_squares(self.legal_moves)
                self.set_state(SELECTMOVE)  # go to move selection
        else:
            self.reset_selection()
        self.set_mouse_pressed(False)

    def handle_move_selection(self):
        # state conditionals
        if self.legal_moves:
            if self.mouse_pressed:
                if self.valid_move_selected(self.mouse_pos, self.legal_moves):
                    # update state variables
                    row, col = self.board.mouse_pos_to_grid(self.mouse_pos)
                    # move the piece
                    self.captured_piece = self.board.move_piece(
                        self.selected_piece, row, col
                    )
                    ## check if piece is a pawn
                    if self.selected_piece.type == "pawn":
                        if (
                            self.selected_piece.row == 0
                            and self.selected_piece.color == WHITE
                        ) or (
                            self.selected_piece.row == 7
                            and self.selected_piece.color == BLACK
                        ):
                            ## active promotion_menu
                            bucket = self.selected_piece
                            self.reset_selection()
                            self.state = SELECTPROMOTION
                            self.selected_piece = bucket
                            # build promotion menu
                            self.build_promotion_menu()
                            self.update_current_player(self.captured_piece)
                        else:
                            self.reset_selection()
                            self.update_current_player(self.captured_piece)
                    else:
                        self.reset_selection()
                        self.update_current_player(self.captured_piece)
                else:
                    self.reset_selection()
        else:
            self.reset_selection()

    def handle_promotion_selection(self):
        if self.promotion_menu:
            if self.mouse_pressed:
                promotion_option = self.promotion_menu.valid_promotion_selected(
                    self.mouse_pos
                )
                if promotion_option != None:
                    ## we now have the promotion option
                    ## create a new piece in the location of the old piece
                    piece_type = self.promotion_menu.image_options[
                        promotion_option
                    ].split(sep="_")[0]
                    if self.selected_piece.color == BLACK:
                        self.dark_team.active_pieces.remove(self.selected_piece)
                        self.selected_piece = self.board.upgrade_piece(
                            self.selected_piece, piece_type
                        )
                        self.dark_team.active_pieces.append(self.selected_piece)
                    else:
                        self.light_team.active_pieces.remove(self.selected_piece)
                        self.selected_piece = self.board.upgrade_piece(
                            self.selected_piece, piece_type
                        )
                        self.light_team.active_pieces.append(self.selected_piece)

                    self.set_mouse_pressed(False)
                    self.reset_selection()
                else:
                    self.mouse_pressed = False
        else:
            self.reset_selection()

    def build_promotion_menu(self):
        self.promotion_menu = PromotionMenu(self.selected_piece.color)

    def reset_selection(self):
        self.set_legal_moves([])
        self.set_selected_piece(None)
        self.set_state(SELECTPIECE)
        self.set_mouse_pressed(False)
        self.board.clear_highlighted_squares()
        self.promotion_menu = None

    def update_current_player(self, captured_piece):
        if self.current_player == self.dark_team:
            if captured_piece:
                self.light_team.active_pieces.remove(captured_piece)
                self.light_team.captured_pieces.append(captured_piece)
            self.current_player = self.light_team
        elif self.current_player == self.light_team:
            if captured_piece:
                self.dark_team.active_pieces.remove(captured_piece)
                self.dark_team.captured_pieces.append(captured_piece)
            self.current_player = self.dark_team

    def render(self):
        self.board.draw_board()  # draw board onto the window
        self.board.draw_highlights(GREEN)
        self.board.draw_pieces()  # draw all pieces onto the board
        if self.promotion_menu:
            self.board.draw_menu(self.promotion_menu)

    ### State methods, might move

    def valid_square_selected(self, mouse_pos: tuple[int, int]) -> bool:
        """
        Method that checks if the mouse position corresponds to a board square.

        Args:
            mouse_pos (tuple[int, int]): The current mouse_pos corresponding to the last mouse press down

        Returns:
            bool : Returns False if outer border of game is selected, otherwise True.

        """
        return self.board.mouse_pos_to_grid(mouse_pos) != (None, None)

    def valid_move_selected(self, mouse_pos, valid_moves):
        return (
            self.valid_square_selected(mouse_pos)
            and self.board.mouse_pos_to_grid(mouse_pos) in valid_moves
        )

    def get_mouse_pressed(self):
        return self.mouse_pressed

    def set_mouse_pressed(self, value):
        self.mouse_pressed = value

    def get_mouse_pos(self):
        return self.mouse_pos

    def set_mouse_pos(self, x, y):
        self.mouse_pos = (x, y)

    def get_selected_piece(self):
        return self.selected_piece

    def set_selected_piece(self, piece):
        self.selected_piece = piece

    def get_legal_moves(self):
        return self.legal_moves

    def set_legal_moves(self, move):
        self.legal_moves = move

    def get_state(self):
        return self.state

    def set_state(self, state):
        self.state = state

    def print_current_player(self):
        if self.current_player == self.dark_team:
            return "Black Player"
        elif self.current_player == self.light_team:
            return "White Player"
