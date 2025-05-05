import pygame
from .constants import (
    BOARDPOSX,
    BOARDPOSY,
    SQUARESIZE,
    EMPTY,
    SQUARECOUNT,
    BLACK,
    WHITE,
    GREEN,
)
from .piece import Piece, Pawn, Knight, Bishop, Rook, Queen, King


class Board:
    """
    Represents an nxn checkered board.
    """

    def __init__(
        self,
        width: int,
        height: int,
        square_count: int,
        color_dark: pygame.Color,
        color_light: pygame.Color,
    ):
        """
        Board is initalized by providing its width and height, and the square_count, the color of
        the dark squares and the color of the light squares, both of which are pygame Color objects.
        Note that square_count refers to the count of squares along either the x axis or y axis.
        ex: if square count is 5, it will be assumed that a 5x5 board is desired.
        """
        self.width: int = width
        self.height: int = height
        self.color_light: pygame.Color = color_light
        self.color_dark: pygame.Color = color_dark
        self.square_count: int = square_count
        self.struct: list = self.__create_board_struct()
        self.surface: pygame.Surface = pygame.Surface((width, height))
        self.highlighted_surface: pygame.Surface = pygame.Surface(
            (width, height), flags=pygame.SRCALPHA
        )
        self.rect: pygame.Rect = self.surface.get_rect(topleft=(BOARDPOSX, BOARDPOSY))
        self.__draw_base_board()
        self.highlighted_squares = []

    def __create_board_struct(self) -> list[list]:
        """
        Creates the "struct" for the board.
        implemented as a list of lists
        Mutates the list as the list is built.
        board.struct[i][j] refers to the ith row, and the jth column of the board.
        Returns : a list of lists
        """
        struct: list = []
        for row_index in range(self.square_count):
            row = []
            for col_index in range(self.square_count):
                row.append(EMPTY)
            struct.append(row)
        return struct

    def __draw_base_board(self):
        """
        draws the board in its initial state
        a checkerboard with light color in top left corner
        """
        # we go through the board and for each square, we "blit" onto the board the current square.
        for row in range(self.square_count):
            for col in range(self.square_count):
                color = self.color_dark if (row + col) % 2 == 1 else self.color_light
                self.color_square(row, col)

    def color_square(self, row_index, col_index, color=None):
        square = pygame.Surface((SQUARESIZE, SQUARESIZE))
        if color == None:
            color = (
                self.color_dark
                if (row_index + col_index) % 2 == 1
                else self.color_light
            )
        square.fill(color)
        self.surface.blit(square, (col_index * SQUARESIZE, row_index * SQUARESIZE))

    def highlight_square(self, row_index, col_index, color, alpha=128):
        square = pygame.Surface((SQUARESIZE, SQUARESIZE), flags=pygame.SRCALPHA)
        square.fill((*color, alpha))
        self.highlighted_surface.blit(
            square, (col_index * SQUARESIZE, row_index * SQUARESIZE)
        )

    def draw_highlights(self, color, surface):
        # clear all highlights
        self.highlighted_surface.fill((0, 0, 0, 0))

        # now redraw highlights
        for square in self.highlighted_squares:
            self.highlight_square(*square, color)

        surface.blit(self.highlighted_surface, (BOARDPOSX, BOARDPOSY))

    def clear_highlights(self):
        self.highlighted_surface.fill((0, 0, 0, 0))

    def color_square(self, row_index, col_index, color=None, highlight=False):
        """
        Colors a given square on the board, creating a square, filling it and blitting it on the board.
        In the case that a color is not given it paints the board with its original
        checkerboard colors
        """
        # checks if square is even or odd, setting even to white and odd to black
        square = pygame.Surface((SQUARESIZE, SQUARESIZE))
        if color == None:
            color = (
                self.color_dark
                if (row_index + col_index) % 2 == 1
                else self.color_light
            )
        if highlight:
            square = pygame.Surface((SQUARESIZE, SQUARESIZE), flags=pygame.SRCALPHA)
            square.fill((color[0], color[1], color[2], 128))
        else:
            square.fill(color)
        self.surface.blit(square, (col_index * SQUARESIZE, row_index * SQUARESIZE))

    def draw_legal_moves(self, moves):
        if not moves:
            return
        for move in moves:
            self.highlight_square(move[0], move[1], GREEN)

    def set_piece(self, piece: Piece):
        """
        sets the piece on the boards data structure during setup of game.
        """
        # ensures board is empty at location.
        if self.struct[piece.row][piece.col] == None:
            self.struct[piece.row][piece.col] = piece
        else:
            raise ValueError(
                f"Piece already exists in row : {piece.row} col : {piece.col}"
            )

    def is_empty(self, row, col):
        if not self.in_bounds(row, col):
            return False
        return self.struct[row][col] == EMPTY

    def get_piece(self, row, col) -> Piece:
        return self.struct[row][col]

    def generate_legal_moves(self, piece):
        """
        prompts the piece to give its valid moves
        If in actuality piece is none returns the empty list.
        Useful for later deletion of valid but illegal moves
        """
        if piece != None:
            return piece.generate_valid_moves(self)
        else:
            return []

    def in_bounds(self, row, col):
        return (0 <= row < SQUARECOUNT) and (0 <= col < SQUARECOUNT)

    def load_pieces(self):
        """
        Loads the piece into their pieces array
        """
        # clear piece arrays
        black_pieces = []
        white_pieces = []
        # generate pawns
        for i in range(SQUARECOUNT):
            black_pawn = Pawn(BLACK, 1, i, "pawn")
            white_pawn = Pawn(WHITE, 6, i, "pawn")
            black_pieces.append(black_pawn)
            white_pieces.append(white_pawn)

        # generate black pieces
        black_rook = Rook(BLACK, 0, 0, "rook")
        black_rook1 = Rook(BLACK, 0, 7, "rook")
        black_knight = Knight(BLACK, 0, 1, "knight")
        black_knight1 = Knight(BLACK, 0, 6, "knight")
        black_bishop = Bishop(BLACK, 0, 2, "bishop")
        black_bishop1 = Bishop(BLACK, 0, 5, "bishop")
        black_king = King(BLACK, 0, 4, "king")
        black_queen = Queen(BLACK, 0, 3, "queen")

        # generate white pieces
        white_rook = Rook(WHITE, 7, 0, "rook")
        white_rook1 = Rook(WHITE, 7, 7, "rook")
        white_knight = Knight(WHITE, 7, 1, "knight")
        white_knight1 = Knight(WHITE, 7, 6, "knight")
        white_bishop = Bishop(WHITE, 7, 2, "bishop")
        white_bishop1 = Bishop(WHITE, 7, 5, "bishop")
        white_king = King(WHITE, 7, 4, "king")
        white_queen = Queen(WHITE, 7, 3, "queen")
        black_pieces += [
            black_rook,
            black_rook1,
            black_knight,
            black_knight1,
            black_bishop,
            black_bishop1,
            black_queen,
            black_king,
        ]
        white_pieces += [
            white_rook,
            white_rook1,
            white_knight,
            white_knight1,
            white_bishop,
            white_bishop1,
            white_queen,
            white_king,
        ]
        return (black_pieces, white_pieces)

    def set_pieces(self, dark_pieces: list[Piece], light_pieces: list[Piece]):
        for black_piece in dark_pieces:
            self.set_piece(black_piece)
        for white_piece in light_pieces:
            self.set_piece(white_piece)

    def move_piece(self, piece: Piece, new_row: int, new_col: int):
        """
        move_piece(self, piece: Piece, new_row : int, new_col : int):
        moves the piece on the boards data  structure.
        updating the pieces data, and the board data.
        Does not draw pieces, simply updates pieces, and board logic.
        returns : None
        """
        old_row = piece.row
        old_col = piece.col
        # Move piece by updating piece parameters
        if piece.is_valid_move(new_row, new_col, self):
            (old_row, old_col) = piece.apply_move(new_row, new_col, self)
            self.struct[old_row][old_col] = None
            self.struct[new_row][new_col] = piece
            self.clear_piece(old_row, old_col)

    def grid_to_rel_pos(self, row: int, col: int) -> tuple:
        """
        grid_to_rel_pos(self, row : int, col : int) -> tuple:
        converts the grid coordinates into a position relative to the board
        returns : a tuple (x,y)
        """
        return (col * SQUARESIZE, row * SQUARESIZE)

    def draw_pieces(self, surface):
        """
        Draws all pieces located on the board
        """
        for row in range(self.square_count):
            for col in range(self.square_count):
                square = self.struct[row][col]
                if square != EMPTY:
                    self.draw_piece(square, row, col, surface)

    def get_abs_pos(self, row, col):
        return (BOARDPOSX + col * SQUARESIZE, BOARDPOSY + row * SQUARESIZE)

    def draw_piece(self, piece: Piece, row: int, col: int, surface):
        """
        draw_piece(self, piece : Piece, row : int , col : int):
        Draws the piece onto the board by first coloring the square under it
        and then drawing the piece over it on the board surface
        returns : None
        """
        pos = self.get_abs_pos(row, col)
        ## first we want to draw a square
        # self.color_square(row, col)
        surface.blit(piece.surface, (pos))

    def mouse_pos_to_grid(self, pos):
        """
        Converts a mouse position to a grid position returning row column tuple
        """
        mouse_x = pos[0]
        mouse_y = pos[1]
        if not self.rect.collidepoint(mouse_x, mouse_y):
            return (None, None)

        col = int((mouse_x - BOARDPOSX) // SQUARESIZE)
        row = int((mouse_y - BOARDPOSY) // SQUARESIZE)

        # handles the rare case that they select right most or bottom most edge,
        # leading to row or column value of 8, illegal
        if 0 <= row < 8 and 0 <= col < 8:
            return (int(row), int(col))
        else:
            return (None, None)

    def clear_piece(self, row: int, col: int):
        """
        clear_piece(self, piece : Piece):
        Clears the piece from the board. "Undrawing" it
        Actually just draws the square over that position
        returns : None
        """
        pos = self.grid_to_rel_pos(row, col)
        color = self.color_dark if (row + col) % 2 == 1 else self.color_light
        self.color_square(row, col)
        # square = pygame.Surface((SQUARESIZE, SQUARESIZE))
        # if (row + col) % 2 == 0:
        #    square.fill(self.color_light)
        # else:
        #    square.fill(self.color_dark)
        # self.surface.blit(square, (col * SQUARESIZE, row * SQUARESIZE))

    def draw_board(self):
        for row in range(SQUARECOUNT):
            for col in range(SQUARECOUNT):
                self.color_square(row, col)

    def undraw_moves(self, moves):
        self.clear_highlights()
        # for move in moves:
        # row = move[0]
        # col = move[1]
        # self.color_square(move[0], move[1])

    def set_highlighted_squares(self, moves):
        self.highlighted_squares = moves

    def clear_highlighted_squares(self):
        self.highlighted_squares = []

    ### State methods, might move

    def valid_piece_selected(self, mouse_pos):
        """
        Checks if a valid piece has been selected
        """
        row, col = self.mouse_pos_to_grid(mouse_pos)
        return (row, col) != (None, None)

    def valid_square_selected(self, mouse_pos):
        return self.mouse_pos_to_grid(mouse_pos) != (None, None)

    def valid_move_selected(self, mouse_pos, valid_moves):
        return (
            self.valid_square_selected(mouse_pos)
            and self.mouse_pos_to_grid(mouse_pos) in valid_moves
        )
