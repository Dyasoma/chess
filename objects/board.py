import pygame
from .constants import BOARDPOSX, BOARDPOSY, SQUARESIZE, EMPTY, SQUARECOUNT, BLACK, WHITE, GREEN
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
        self.surface: pygame.Surface = self.__create_board_surface()
        self.rect: pygame.Rect = self.__create_board_rect()


    def __create_board_struct(self) -> list[list]:
        """
        Creates the instance attribute "struct" for the board object of class Board.
        refers to the boards data structure, implemented as a list of lists
        Mutates the list as the list is built.
        board.struct[i][j] refers to the ith row, and the jth column of the board.
        Returns : a list of lists
        Side effect : creates instance attribute "struct" and mutates it
        """
        struct: list = []
        for row_index in range(self.square_count):
            row = []
            for col_index in range(self.square_count):
                row.append(None)  # Each entry will be None. i.e. empty
            struct.append(row)
        return struct

    def __create_board_surface(self) -> pygame.Surface:
        """
        create_board_surface(self):
        creates the board surface, using the pygame Surface object class, and assigning the returned
        surface as an instance attribute of the board object.
        Creates a black surface.
        blits square from struct attribute onto surface attribute.
        Serves as the "image" of the board.
        Returns : pygame Surface object
        """
        # Surf is first the entire size of the board
        surf = pygame.Surface((self.width, self.height))

        # we go through the board and for each square, we "blit" onto the board the current square.
        for row_index in range(self.square_count):
            for col_index in range(self.square_count):
                self.draw_square(surf, row_index, col_index)
        return surf

    def __create_board_rect(self) -> pygame.Rect:
        """
        create_board_rect(self)
        Creates an instance attribute of object Board, using the instance attribute surface.
        Acts as a wrapper to the get_rect() function for objects of class Surface from pygame module
        returns : pygame rect object
        """
        rec = self.surface.get_rect(topleft=(BOARDPOSX, BOARDPOSY))
        return rec

    def draw_square(self, surf, row_index, col_index, color = None):
        # checks if square is even or odd, setting even to white and odd to black
        if color == None:
            if ((row_index + col_index) % 2) == 0:
                square = pygame.Surface((SQUARESIZE, SQUARESIZE))
                square.fill(self.color_light)
                surf.blit(square, (col_index * SQUARESIZE, row_index * SQUARESIZE))
            else:
                square = pygame.Surface((SQUARESIZE, SQUARESIZE))
                square.fill(self.color_dark)
                surf.blit(square, (col_index * SQUARESIZE, row_index * SQUARESIZE))
        else:
                square = pygame.Surface((SQUARESIZE, SQUARESIZE))
                square.fill(color)
                surf.blit(square, (col_index * SQUARESIZE, row_index * SQUARESIZE))


    def draw_valid_moves(self, moves):
        if not moves:
            return
        for move in moves:
            self.draw_square(self.surface, move[0], move[1], GREEN)

    def set_piece(self, piece : Piece):
        """
        set_piece(self, piece: Piece, new_row : int, new_col : int):
        sets the piece on the boards data structure.
        updating the pieces data, and the board data.
        returns : None
        """
        #ensures board is empty at 
        '''
        if self.struct[new_row][new_col] == None:
            piece.set_row_col(new_row, new_col) # updates piece parameters
            self.struct[new_row][new_col] = piece # places piece object onto board structure
        else:
            print(f"Piece already exists in row : {new_row} col : {new_col}")
        '''
        if self.struct[piece.row][piece.col] == None:
            self.struct[piece.row][piece.col] = piece
        else:
            print(f"Piece already exists in row : {piece.row} col : {piece.col}")

    def is_empty(self, row, col):
        if not self.in_bounds(row, col):
            return False
        return self.struct[row][col] == EMPTY


    def get_piece(self, row, col) -> Piece:
        return self.struct[row][col]
    

    def in_bounds(self, row, col):
        return (((0 <= row < SQUARECOUNT ) and (0 <= col < SQUARECOUNT)))


    def load_pieces(self, black_pieces : list[Piece], white_pieces : list[Piece]):
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
        black_pieces += [black_rook, black_rook1, black_knight, black_knight1, black_bishop, black_bishop1, black_queen, black_king]
        white_pieces += [white_rook, white_rook1, white_knight, white_knight1, white_bishop, white_bishop1, white_queen, white_king]

        for black_piece in black_pieces:
            self.set_piece(black_piece)
        for white_piece in white_pieces:
           self.set_piece(white_piece)

    def move_piece(self, piece : Piece, new_row : int, new_col : int):
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
        if piece.is_legal_move(new_row, new_col, self):
            (old_row, old_col) = piece.apply_move(new_row, new_col, self)
            self.struct[old_row][old_col] = None
            self.struct[new_row][new_col] = piece
            self.clear_piece(old_row, old_col)
        

    def grid_to_rel_pos(self, row : int, col : int) -> tuple:
        """
        grid_to_rel_pos(self, row : int, col : int) -> tuple:
        converts the grid coordinates into a position relative to the board
        returns : a tuple (x,y)
        """
        return (col * SQUARESIZE, row * SQUARESIZE)
    
    def draw_pieces(self):
        """
        Draws all pieces located on the board
        """
        for row in range(self.square_count):
            for col in range(self.square_count):
                square = self.struct[row][col]
                #if square == EMPTY:
                #    self.clear_piece(row, col)
                #else:
                #    self.draw_piece(square, row, col)
                if square != EMPTY:
                    self.draw_piece(square, row, col)

    def draw_piece(self, piece : Piece, row : int, col : int):
        """
        draw_piece(self, piece : Piece, row : int , col : int):
        Draws the piece onto the board. 
        returns : None
        """
        pos = self.grid_to_rel_pos(row, col)
        self.surface.blit(piece.surface, pos)

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
    



    def clear_piece(self, row : int, col : int):
        """
        clear_piece(self, piece : Piece):
        Clears the piece from the board. "Undrawing" it
        Actually just draws the square over that position
        returns : None
        """
        pos = self.grid_to_rel_pos(row, col)
        self.draw_square(self.surface, row, col)
        #square = pygame.Surface((SQUARESIZE, SQUARESIZE))
        #if (row + col) % 2 == 0:
        #    square.fill(self.color_light)
        #else:
        #    square.fill(self.color_dark)
        #self.surface.blit(square, (col * SQUARESIZE, row * SQUARESIZE))
         
    

    def draw_board(self, window : pygame.Surface) -> None:
        """
        draw_board(self, window : pygame.Surface):
        Draws the board onto the pygame surface object called window. 
        Blits the board onto the window
        returns : None
        """
        window.blit(self.surface, (BOARDPOSX, BOARDPOSY))
    def undraw_moves(self, moves):
        for move in moves:
            self.draw_square(self.surface, move[0], move[1])