from .constants import SQUARECOUNT, BLACK, WHITE, BLACKPLAYER, WHITEPLAYER
from .piece import Pawn, Rook, Bishop, Knight, King, Queen
import pygame


class Team:
    def __init__(self, team_num, color):
        self.team_num = team_num
        self.color = color
        self.active_pieces = self.__set_pieces()
        self.captured_pieces = []

    def __set_pieces(self):
        pieces = []
        position_delta = 0
        pawn_position_delta = 1
        if self.team_num == WHITEPLAYER:
            position_delta += SQUARECOUNT - 1
            pawn_position_delta = position_delta - 1
        for i in range(SQUARECOUNT): 
            pawn = Pawn(self.color, pawn_position_delta, i, "pawn")
            pieces.append(pawn)
        rook = Rook(self.color, position_delta, 0, "rook")
        rook1 = Rook(self.color, position_delta, 7, "rook")
        knight = Knight(self.color, position_delta, 1, "knight")
        knight1 = Knight(self.color, position_delta, 6, "knight")
        bishop = Bishop(self.color, position_delta, 2, "bishop")
        bishop1 = Bishop(self.color, position_delta, 5, "bishop")
        king = King(self.color, position_delta, 4, "king")
        queen = Queen(self.color, position_delta, 3, "queen")
        pieces += [
            rook, 
            rook1,
            knight,
            knight1,
            bishop,
            bishop1,
            queen,
            king,
        ]
        return pieces

    def get_active_pieces(self):
        return len(self.active_pieces)

    def get_captured_pieces(self):
        return len(self.captured_pieces)
