import pygame
from .constants import (
    BOARDPOSX,
    BOARDPOSY,
    ALPHA_FLAG,
    SQUARESIZE,
    SQUARECOUNT,
    PIECE_ROOK,
    PIECE_BISHOP,
    PIECE_KNIGHT,
    PIECE_QUEEN,
)
from .piece import Piece, Pawn, Knight, Bishop, Rook, Queen, King


class Board:
    """
    Represents a NxN checkerboard 

    Args:
        square_size (int): The pixel size of each individual square
        square_count (int): The number of squares in a given row or column i.e. board is square_count x square_count
        color_dark (pygame.Color): The color of the dark squares
        color_light (pygame.Color): The color of the light squares
        window (pygame.Surface): The game window's surface

    Attributes:
        struct (list[list[Piece | None]]): 2D grid storing pieces or None 
        surface (pygame.Surface): Base surface / Image of the board
        highlighted_surface (pygame.Surface): Transparent overlay surface for highlighting
        rect (pygame.Rect): Position and size of the board relative to the window
        highlighted_squares list[tuple[int, int]]: Squares which are to be highlighted stored as a list of (row,col) tuples. 

    """
    def __init__(
        self,
        square_size: int,
        square_count: int,
        color_dark: pygame.Color,
        color_light: pygame.Color,
        window : pygame.Surface
    ):

        self.square_size = square_size
        self.color_light: pygame.Color = color_light
        self.color_dark: pygame.Color = color_dark
        self.square_count: int = square_count
        self.struct: list[list[Piece | None]] = self._create_board_struct()
        self.window : pygame.Surface = window
        self.surface: pygame.Surface = pygame.Surface((square_count * square_size, square_count * square_size))
        self.highlighted_surface: pygame.Surface = pygame.Surface(
            (square_size, square_size), flags=ALPHA_FLAG
        )
        self.rect: pygame.Rect = self.surface.get_rect(topleft=(BOARDPOSX, BOARDPOSY))
        self._draw_base_board()
        self.highlighted_squares: list[tuple[int, int]]  = []

    def _create_board_struct(self) -> list[list[Piece | None]]:
        """
        Initializes the structure of the board as a 2D list.
        Each element of the list is either a Piece object or None which represents an empty square.

        Returns:
            list[list[Piece | None]]: a square_count x square_count Grid
        """
        struct = []
        for row_index in range(self.square_count):
            row = []
            for col_index in range(self.square_count):
                row.append(None)
            struct.append(row)
        return struct

    def _draw_base_board(self):
        """
        Colors the board with a checkerboard style, with the first (top-left) square being the self.light_color 
        """
        # we go through the board and for each square, we "blit" onto the board the current square.
        for row in range(self.square_count):
            for col in range(self.square_count):
                self.color_square(row, col)

    def highlight_square(self, row_index : int, col_index : int, color : pygame.Color, alpha=128):
        """
        Highlights an individual square by drawing over the semi-transparent highlighted surface

        Args:
            row_index (int): The row index of the square to highlight
            col_index (int): The col index of the square to highlight
            color (pygame.Color): The highlight Color
            alpha (int): Transparency level from 0-255, Optional. Defaults to 128
        """
        square = pygame.Surface((SQUARESIZE, SQUARESIZE), flags=ALPHA_FLAG)
        square.fill((*color, alpha))
        self.highlighted_surface.blit(
            square, (col_index * SQUARESIZE, row_index * SQUARESIZE)
        )

    def draw_highlights(self, color : pygame.Color):
        """
        Clears highlights and redraws highlights onto the highlight surface

        Args:
            color (pygame.Color): The color used to highlight the entire surface
        """
        self.clear_highlights()
        for square in self.highlighted_squares:
            self.highlight_square(*square, color)
        self.window.blit(self.highlighted_surface, (BOARDPOSX, BOARDPOSY))

    def clear_highlights(self):
        self.highlighted_surface.fill((0, 0, 0, 0))

    def color_square(self, row_index : int, col_index : int, color : pygame.Color = None, highlight: bool =False):
        """
        Colors an individual square on the board.
        If no color is provided it colors based on the default checkerboard pattern and its (row, col) position
        If highlight is True, a semi-transparent version of the color is provided

        Args:
            row_index (int) : The row index of the square
            col_index (int) : the col_index of the square
            Color (pygame.Color, optional) : the color of the square, if None defaults to dark / light
            highlight (bool, optional) : Flag to check if semi-transparent highlight is used. Default is False
        
        """
        square = pygame.Surface((SQUARESIZE, SQUARESIZE))
        if color is None:
            color = self.color_dark if (row_index + col_index) % 2 == 1 else self.color_light
        flags = ALPHA_FLAG if highlight else 0  
        square = pygame.Surface((SQUARESIZE, SQUARESIZE), flags=flags)
        if highlight:
            square.fill(*color, 128)
        else:
            square.fill(color)
        self.surface.blit(square, (col_index * SQUARESIZE, row_index * SQUARESIZE))

            

    def set_piece(self, piece: Piece):
        """
        Places piece on the board at its specified (row, col) position
        This method is used during setup of games, not for movement of pieces.


        Args:
            piece (Piece) : The piece object with its 'row' and 'col' attributes set

        Raises:
            ValueError: If the target square is already filled
            IndexError: If the specififed location is out of bounds
        """
        # ensures board is empty at location.
        row, col = piece.row , piece.col

        if not self.in_bounds(row, col):
            raise IndexError(f"Board position out of bounds: ({row}, {col})")
        

        if self.struct[row][col] is None:
            self.struct[row][col] = piece
        else:
            raise ValueError(
                f"Square is occupied at ({row}, {col})"
            )


    def get_square_contents(self, row : int, col : int) -> Piece | None:
        """
        Returns the piece at the board position board(row, col), or None if the square is empty
        input : 
            row (int) : 0-indexed
            col (int) : 0-indexed
        Raises :
            ValueError if row or column are out of bounds
        """
        if not (0 <= row < SQUARECOUNT and 0 <= col < SQUARECOUNT): 
            raise ValueError("Invalid row or column") 
        return self.struct[row][col]

    def generate_legal_moves(self, piece : Piece | None) -> list[tuple[int, int]]:
        """
        Returns the legal moves for a given piece. 
        
        Currently only returns valid moves as determined by the piece.
        In the future it will filter out moves that are illegal. i.e. a move that would lead to a checkmate.

        Args: 
            piece (Piece | None): the given piece. If the piece does not exist returns the empty list.
        Returns:
            list[tuple[int, int]]: a list of legal moves positions stored as (row, col) tuples.
        """
        if piece is not None:
            return piece.generate_valid_moves(self)
        else:
            return []

    def in_bounds(self, row : int , col : int) -> bool:
        """
        Returns if a position is contained within the board
        Args:
            row(int): The positions row
            col(int): The positions col
        """
        return (0 <= row < SQUARECOUNT) and (0 <= col < SQUARECOUNT)

    def set_pieces(self, dark_pieces: list[Piece], light_pieces: list[Piece]):
        """
        Sets the dark pieces and light pieces for the corresponding players. 
        
        Assumes each piece has their 'row' and 'col' attributes setup
        
        This method is only used for setting up all pieces, not moving groups of pieces. 

        Args:
            dark_pieces(list[Piece]): The pieces for the player who plays the dark pieces
            light_pieces(list[Piece]): The pieces for the player who plays the light pieces

        Raises:
            ValueError: If a piece is a placed on a square that is already occupied
        """
        for black_piece in dark_pieces:
            self.set_piece(black_piece)
        for white_piece in light_pieces:
            self.set_piece(white_piece)

    def move_piece(self, piece: Piece, dest_row: int, dest_col: int) -> Piece | None:
            """
            moves the given piece by updating both the pieces attributes and the boards structure.
            If a piece is located at the destination square, it is "captured" by removing it from the board structure
            and is returned. 

            This method does not handle drawing or rendering only piece and board logic. 

            Args:
                piece (Piece): The piece that is being moved
                dest_row (int): The row the piece will move to
                dest_col (int): THe col the piece will move to
            
            Returns:
                (Piece | None): Returns a captured piece if any, else returns None
            """
            # Move piece by updating piece parameters
            if piece.is_valid_move(dest_row, dest_col, self):
                captured_piece = self.get_square_contents(dest_row, dest_col)
                (old_row, old_col) = piece.apply_move(dest_row, dest_col) # update piece parameters
                # update board parameters
                self.struct[old_row][old_col] = None
                self.struct[dest_row][dest_col] = piece
                return captured_piece


    def upgrade_piece(self, piece : Piece, dest_type : str) -> Piece:
        """
        
        """
        row, col, color = piece.color, piece.row, piece.col, piece.color
        upgrade_selection = {
            PIECE_ROOK : Rook,
            PIECE_BISHOP : Bishop,
            PIECE_KNIGHT : Knight,
            PIECE_QUEEN : Queen
        }
        if dest_type not in upgrade_selection:
            raise ValueError(f"Invalid upgrade type : {dest_type}")
        piece_class = upgrade_selection[dest_type]
        new_piece = piece_class(color, row, col, dest_type)
        self.struct[new_piece.row][new_piece.col] = new_piece
        return new_piece


    def draw_pieces(self):
        """
        Draws all pieces located on the board
        """
        for row in range(self.square_count):
            for col in range(self.square_count):
                square = self.struct[row][col]
                if square != None:
                    self.draw_piece(square, row, col, self.window)

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

    def draw_board(self):
        #for row in range(SQUARECOUNT):
            #for col in range(SQUARECOUNT):
                #self.color_square(row, col)
        self.window.blit(self.surface, (BOARDPOSX, BOARDPOSY))


    def draw_menu(self, promo):
        self.window.blit(promo.surface, (promo.x + BOARDPOSX, promo.y + BOARDPOSY))

    def undraw_moves(self):
        self.clear_highlights()

    def set_highlighted_squares(self, moves):
        self.highlighted_squares = moves

    def clear_highlighted_squares(self):
        self.highlighted_squares = []



    ### State methods, might move

    def valid_square_selected(self, mouse_pos):
        return self.mouse_pos_to_grid(mouse_pos) != (None, None)

    def valid_move_selected(self, mouse_pos, valid_moves):
        return (
            self.valid_square_selected(mouse_pos)
            and self.mouse_pos_to_grid(mouse_pos) in valid_moves
        )
