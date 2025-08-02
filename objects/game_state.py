from .constants import (
    STARTTURN,
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
        other_player (int): The player whose is waiting for their turn
        promotion_menu (PromotionMenu): The object representing the upgrade menu once a pawn reaches the enemy main rank.

    """

    def __init__(self, board: Board, dark_team: Team, light_team: Team):
        self.mouse_pressed = False
        self.mouse_pos: tuple[int, int] = (0, 0)
        self.selected_piece: Piece | None = None # Selected piece for highlighting and moving of pieces
        self.captured_piece: Piece | None = None # captured pieces during current players turn
        self.legal_moves: list[tuple[int, int]] = [] # legal moves the current player can make
        self.checking_pieces : dict[Piece, tuple[int, int]] # pieces of the other player that are checking the current player
        self.state: int = SELECTPIECE # state variable 
        self.board: Board = board
        self.dark_team: Team = dark_team
        self.light_team: Team = light_team
        self.current_player: Team = self.light_team
        self.other_player: Team = self.dark_team
        self.promotion_menu = None

    def handle_events(self):
        """
        Handles the pygame side of events
        """
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                self.set_mouse_pressed(True)
                self.set_mouse_pos(*pygame.mouse.get_pos())

    def update_state(self):
        ## Note that these method depends on hook methods, i.e. the on_enter_new_state method.
        ## To handle changes when entering a new state
        if self.state == STARTTURN:
            self.handle_turn_start()
        elif self.state == SELECTPIECE:
            self.handle_piece_selection()
        elif self.state == SELECTMOVE:
            self.handle_move_selection()
        elif self.state == SELECTPROMOTION:
            self.handle_promotion_selection()

    def change_state(self, new_state: int):
        self.state = new_state
        self.on_enter_new_state(self.state)

    def on_enter_new_state(self, state: int):
        """
        A hook method. Whenever we change states, sometimes it is necessary to accomplish some task,
        This method does just that, and ensure that for each state, the body of the conditional doesn't need to be
        repeated

        Contains the actual "actions" of a given state
        """
        self.set_mouse_pressed(False) #????
        if state == SELECTMOVE:
            self.set_legal_moves(self.board.generate_legal_moves(self.selected_piece))
            self.board.set_highlighted_squares(self.legal_moves)
        if state == SELECTPROMOTION:
            """
            Bottom two lines remove selected squares during promotion, must consider something different
            """
            # self.board.set_highlighted_squares([]) # ui
            self.board.clear_highlighted_squares() # clear highlighted squares
            self.build_promotion_menu()  # actually necessary function call.
        if state == SELECTPIECE:
            return

    def handle_piece_selection(self):
        """
        Piece selection state
        
        """
        if self.mouse_pressed: # event
            # validate event
            if self.valid_square_selected(self.mouse_pos):
                row, col = self.board.mouse_pos_to_grid(
                    self.mouse_pos
                )  # convert to grid positions
                if not self.board.is_empty(row, col):
                    self.set_selected_piece(self.board.get_square_contents(row, col))
                    if self.selected_piece and self.current_player.owns(
                        self.selected_piece
                    ):
                        self.change_state(SELECTMOVE)  # go to move selection
                    else:
                        self.reset_turn(f"{self.print_current_player()} does not own the selected piece")
                else:
                    self.reset_turn("Board is empty at selected location")
            else:
                self.reset_turn("No Valid Square was selected")
        else:
            self.continue_in_state()

    def handle_move_selection(self):
        """
        Move selection after a piece has been selected

        Note: Valid moves are generated in the 'on_enter_new_state' method
        """
        # generate associated move data
        if self.mouse_pressed: # event
            # validate event 
            if self.legal_moves:    
                if self.valid_square_selected(self.mouse_pos):
                    row, col = self.board.mouse_pos_to_grid(self.mouse_pos)
                    if self.valid_move_selected(row, col, self.legal_moves):
                        self.captured_piece = self.board.move_piece(
                            self.selected_piece, row, col
                        )
                        if self.selected_piece.is_promotable():
                            print("You can promote your piece!")
                            self.change_state(SELECTPROMOTION)
                        else:
                            self.end_turn()
                    else:
                        self.reset_turn("Invalid move for selected piece")
                else:
                    self.reset_turn("Invalid Square Selected")
            else:
                self.reset_turn("Piece has no valid moves")
        else:
            self.continue_in_state()

    def handle_promotion_selection(self):
        """
        Promotion of a pawn into a new piece, must occur.
        """
        assert (
            self.promotion_menu is not None
        ), "Promotion Menu must exist in the SELCTPROMOTION state"
        if self.mouse_pressed:
            promotion_option = self.promotion_menu.get_valid_promotion_option(
                self.mouse_pos
            )
            if promotion_option != None:
                new_type = self.promotion_menu.get_piece_type(promotion_option)
                self.board.upgrade_piece(
                    self.current_player, self.selected_piece, new_type
                )
                self.end_turn()
            else:
                print("Invalid promotion option")
                self.set_mouse_pressed(False)
        else:
            self.continue_in_state()

    def end_turn(self):
        self.update_current_player(self.captured_piece)
        self.reset_turn()

    def build_promotion_menu(self):
        self.promotion_menu = PromotionMenu(self.selected_piece.color)

    def reset_turn(self, msg: str = None):
        self.reset(msg)
        self.change_state(SELECTPIECE)

    def continue_in_state(self):
        # does nothing, exists to make non-response explicitly do nothing. 
        pass

    def reset(self, msg = None):
        if msg:
            print(f"{msg}")
        self.set_legal_moves([])
        self.set_selected_piece(None)
        self.board.clear_highlighted_squares()
        self.change_state(SELECTPIECE)
        self.set_mouse_pressed(False)
        self.promotion_menu = None

    def update_current_player(self, captured_piece):
        """
        Changes the current player into the other player. i.e. changes the active player from white to black
        """
        if captured_piece:
            self.other_player.active_pieces.remove(captured_piece)
            self.other_player.captured_pieces.append(captured_piece)
        if self.current_player.color == WHITE:
            print("It is now Black's turn")
            self.current_player = self.dark_team
            self.other_player = self.light_team
        else:
            print("It is now White's turn")
            self.current_player = self.light_team
            self.other_player = self.dark_team

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

    def valid_move_selected(self, row, col, valid_moves):
        return (row, col) in valid_moves

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



    def print_current_player(self):
        if self.current_player == self.dark_team:
            return "Black Player"
        elif self.current_player == self.light_team:
            return "White Player"
