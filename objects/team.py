import pygame
from .constants import (
    SQUARECOUNT,
    WHITEPLAYER,
    PIECE_ROOK,
    PIECE_KNIGHT,
    PIECE_BISHOP,
    PIECE_QUEEN,
)
from .piece import Piece, Pawn, Rook, Bishop, Knight, King, Queen


class Team:
    """
    Represents a "team" of pieces.

    Args:
        team_id (int): The team ID, 0 represents dark pieces and 1 represents light pieces.
        color (pygame.Color): The color of the associated pieces.

    Attributes:
        team_id (int): The team ID, 0 represents dark pieces and 1 represents light pieces.
        color (pygame.Color): The color of the associated pieces.
        active_pieces (list[Piece]): A list of pieces that are currently in play
        captured_pieces (list[Piece]): A list of pieces that belong to the player and have been captured.
    """

    def __init__(self, team_id: int, color: pygame.Color):
        self.team_id: int = team_id
        self.color: pygame.Color = color
        self.active_pieces: list[Piece] = self._set_pieces()
        self.captured_pieces: list[Piece] = []

    def _set_pieces(self):
        """
        Used to setup each pieces data, does not modify board, only internal piece data.

        Can be used to reset all pieces for a given player / team.
        """
        pieces = []
        self.captured_pieces = []
        if self.team_id == WHITEPLAYER:
            main_rank = 7
            pawn_rank = 6
        else:
            main_rank = 0
            pawn_rank = 1

        for i in range(SQUARECOUNT):
            pawn = Pawn(self.color, pawn_rank, i, "pawn")
            pieces.append(pawn)
        rook = Rook(self.color, main_rank, 0, "rook")
        rook1 = Rook(self.color, main_rank, 7, "rook")
        knight = Knight(self.color, main_rank, 1, "knight")
        knight1 = Knight(self.color, main_rank, 6, "knight")
        bishop = Bishop(self.color, main_rank, 2, "bishop")
        bishop1 = Bishop(self.color, main_rank, 5, "bishop")
        king = King(self.color, main_rank, 4, "king")
        queen = Queen(self.color, main_rank, 3, "queen")
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

    def owns(self, piece: Piece) -> bool:
        """
        Checks that a piece belongs to a given team, Returns True if the piece has the same color as the team

        Args:
            piece (Piece): The piece that we are comparing to,

        """
        return self.color == piece.color

    def get_count_active(self):
        return len(self.active_pieces)

    def get_count_captured(self):
        return len(self.captured_pieces)


