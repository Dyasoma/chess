import pygame
from .constants import WHITE, BLACK, SQUARESIZE, EMPTY, BOARDPOSX, BOARDPOSY


class Piece:
    def __init__(self, color: pygame.Color, row: int, col: int, type: str):
        """
        Class used to represent a chess piece.
        """
        self.size = SQUARESIZE
        self.type = type
        self.row = row
        self.col = col
        self.color = color
        self.surface = self.__create_piece_surface()
        self.rect = pygame.Rect(
            BOARDPOSX + SQUARESIZE * col,
            BOARDPOSY + SQUARESIZE * row,
            SQUARESIZE,
            SQUARESIZE,
        )

    def __create_piece_surface(self) -> pygame.Surface:
        """
        __create_piece_surface(self) -> pygame.Surface:
        Creates the surface instance attribute for the given piece
        First loading an image depending on the piece type
        Then scales the image
        returns : pygame surface object for the image of the piece
        """
        if self.color == WHITE:
            surface = pygame.image.load(f"./Assets/{self.type}_white.png")
        else:
            surface = pygame.image.load(f"./Assets/{self.type}_black.png")
        return pygame.transform.smoothscale(surface, (self.size, self.size))

    def __create_piece_rect(self) -> pygame.Rect:
        """
        __create_piece_rect(self) -> pygame.Rect:
        creates a pygame rect object for the instance attribute rect
        returns : a pygame rect object
        """

    def set_row_col(self, row, col):
        """
        set(self, init_col, init_row):
        sets the pieces row and column elements.
        """
        self.row = row
        self.col = col

    def is_valid_move(self, new_row, new_col, board):
        return (new_row, new_col) in self.generate_valid_moves(board)

    def apply_move(self, new_row, new_col, board):
        # first update piece parameters
        old_row = self.row
        old_col = self.col
        self.row = new_row
        self.col = new_col
        return (old_row, old_col)

    def generate_valid_moves(self, board):
        # exists purely to be over written by subclasses
        raise NotImplementedError

    def get_sliding_moves(self, board, directions):
        valid_moves = []
        new_row = self.row
        new_col = self.col
        for dr, dc in directions:
            new_row = self.row + dr
            new_col = self.col + dc
            while board.in_bounds(new_row, new_col):
                # now validate
                found_piece = board.get_piece(new_row, new_col)
                if not found_piece:  # no piece, add move
                    valid_moves.append((new_row, new_col))
                elif (
                    found_piece.color != self.color
                ):  # found a piece check if ally or enemy
                    valid_moves.append((new_row, new_col))
                    break
                else:
                    break
                new_row += dr
                new_col += dc
        return valid_moves


class Pawn(Piece):
    def __init__(self, color: pygame.Color, row: int, col: int, type: str):
        super().__init__(color, row, col, type)
        self.has_moved = False

    def generate_valid_moves(self, board):
        ## generates a list of valid moves
        valid_moves = []
        ## generate valid 1 and 2 motion moves.
        dv = -1 if self.color == WHITE else 1  # vertical direction
        one_forward = self.row + dv
        two_forward = self.row + (dv * 2)

        ## single jump moves
        if board.is_empty(one_forward, self.col):
            valid_moves.append((one_forward, self.col))

            ## double jump moves
            if not self.has_moved:
                if board.is_empty(two_forward, self.col):
                    valid_moves.append((two_forward, self.col))

        ## generate diagonal taking moves
        for dh in [-1, 1]:
            if not board.in_bounds(one_forward, self.col + dh):
                continue
            # we are now in bound of square
            if board.is_empty(one_forward, self.col + dh):
                continue
            # new position now has a possible piece to take
            takeable_piece = board.get_piece(one_forward, self.col + dh)
            if takeable_piece and takeable_piece.color != self.color:
                # new position has enemy piece, add diagonal
                valid_moves.append((one_forward, self.col + dh))

        return valid_moves

    def apply_move(self, new_row, new_col, board):
        self.has_moved = True
        return super().apply_move(new_row, new_col, board)


class Knight(Piece):
    def __init__(self, color: pygame.Color, row: int, col: int, type: str):
        super().__init__(color, row, col, type)

    def generate_valid_moves(self, board):
        ## generates a list of valid moves
        valid_moves = []
        delta_array = [2, 1, -2, -1]
        ## check the delta
        ## completes a pairwise generation of deltas for the row and columns
        ## skips values where the deltas are equal, as knights move in a l direction
        ## this implies deltas are at least different in magnitude (1, 2) or are different in magnitude and sign (2, -1)
        for i in delta_array:
            for j in delta_array:
                if (
                    i == j
                ):  # same delta, 1 and 1 would be equivalent to a knight moving down 1 and right 1, which isn't correct
                    continue
                if (
                    i == -j
                ):  # -1 and 1 shouldn't be evaluated as a knight cannot move up 1 and right 1,
                    continue
                new_row = self.row + i
                new_col = self.col + j
                if board.in_bounds(new_row, new_col):  # actually on the board
                    found_piece = board.get_piece(new_row, new_col)
                    if not found_piece or found_piece.color != self.color:
                        valid_moves.append((new_row, new_col))
        return valid_moves


class Bishop(Piece):
    def __init__(self, color: pygame.Color, row: int, col: int, type: str):
        super().__init__(color, row, col, type)

    def generate_valid_moves(self, board):
        diagonals = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        return self.get_sliding_moves(board, diagonals)


class Rook(Piece):
    def __init__(self, color: pygame.Color, row: int, col: int, type: str):
        super().__init__(color, row, col, type)
        self.has_moved = False

    def generate_valid_moves(self, board):
        cardinals = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        return self.get_sliding_moves(board, cardinals)

    def apply_move(self, new_row, new_col, board):
        self.has_moved = True
        return super().apply_move(new_row, new_col, board)


class Queen(Piece):
    def __init__(self, color: pygame.Color, row: int, col: int, type: str):
        super().__init__(color, row, col, type)

    def generate_valid_moves(self, board):
        cardinals = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        diagonals = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        return self.get_sliding_moves(board, cardinals + diagonals)


class King(Piece):
    def __init__(self, color: pygame.Color, row: int, col: int, type: str):
        super().__init__(color, row, col, type)
        self.has_moved = False

    def generate_valid_moves(self, board):
        valid_moves = []
        cardinals = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        diagonals = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        directions = cardinals + diagonals
        for dr, dc in directions:
            new_row = self.row + dr
            new_col = self.col + dc
            if board.in_bounds(new_row, new_col):
                # now validate
                found_piece = board.get_piece(new_row, new_col)
                if (
                    not found_piece or found_piece.color != self.color
                ):  # no piece, add move
                    valid_moves.append((new_row, new_col))

        return valid_moves

    def apply_move(self, new_row, new_col, board):
        self.has_moved = True
        return super().apply_move(new_row, new_col, board)
