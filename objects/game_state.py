from .constants import SELECTPIECE, SELECTMOVE, GREEN, BOARDPOSX, BOARDPOSY
from .board import Board
from pygame.locals import *
import pygame
import sys
class GameState:
    def __init__(self, board : Board, black_team, white_team):
        self.mouse_pressed = False
        self.mouse_pos = (None, None)
        self.selected_piece = None 
        self.captured_piece = None
        self.legal_moves = []
        self.state = SELECTPIECE
        self.board = board
        self.black_team = black_team
        self.white_team = white_team
        self.current_player = self.white_team

    def handle_events(self):
        for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == MOUSEBUTTONDOWN:
                    # get the mouse position
                    self.set_mouse_pressed(True)
                    self.set_mouse_pos(*pygame.mouse.get_pos())


    def handle_piece_selection(self):
        # state conditionals
        if self.mouse_pressed and self.board.valid_square_selected(
            self.mouse_pos
        ):  # mouse is pressed
            # update state variable
            row, col = self.board.mouse_pos_to_grid(self.mouse_pos)
            self.set_selected_piece(self.board.get_piece(row, col))
            ## we now have a piece, check that it is valid for the given player
            if self.selected_piece and self.selected_piece.color == self.current_player.team_color:
                self.set_legal_moves(self.board.generate_legal_moves(self.selected_piece))
                self.board.set_highlighted_squares(self.legal_moves)
                self.set_state(SELECTMOVE)  # go to move selection
            # sanitize
            self.set_mouse_pressed(False)
    
    def handle_move_selection(self):
    # state conditionals
        if self.legal_moves:
            if self.mouse_pressed:
                if self.board.valid_move_selected(self.mouse_pos, self.legal_moves):
                    # update state variables
                    row, col = self.board.mouse_pos_to_grid(self.mouse_pos)
                    # move the piece
                    self.captured_piece = self.board.move_piece(self.selected_piece, row, col)
                    self.reset_selection()
                    self.update_current_player(self.captured_piece)
                else:
                    self.reset_selection()
        else:
            self.reset_selection()

    def update_logic(self,):
        if self.state == SELECTPIECE:
            self.handle_piece_selection()
        elif self.state == SELECTMOVE:
            self.handle_move_selection()


    def reset_selection(self):
        self.set_legal_moves([])
        self.set_selected_piece(None)
        self.set_state(SELECTPIECE)
        self.set_mouse_pressed(False)
        self.board.clear_highlighted_squares()

    def update_current_player(self, captured_piece):
        if self.current_player == self.black_team:
            if captured_piece:
                self.white_team.active_pieces.remove(captured_piece)
                self.white_team.captured_pieces.append(captured_piece)
            self.current_player = self.white_team
        elif self.current_player == self.white_team:
            if captured_piece:
                self.black_team.active_pieces.remove(captured_piece)
                self.black_team.captured_pieces.append(captured_piece)
            self.current_player = self.black_team

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
        if self.current_player == self.black_team:
            return 'Black Player'
        elif self.current_player == self.white_team:
            return 'White Player'