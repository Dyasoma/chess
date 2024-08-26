import pygame
from .constants import BOARDPOSX, BOARDPOSY, SQUARESIZE
from .piece import Piece


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
                # checks if square is even or odd, setting even to white and odd to black
                if (row_index + col_index) % 2 == 0:
                    square = pygame.Surface((SQUARESIZE, SQUARESIZE))
                    square.fill(self.color_dark)
                    surf.blit(square, (col_index * SQUARESIZE, row_index * SQUARESIZE))
                else:
                    square = pygame.Surface((SQUARESIZE, SQUARESIZE))
                    square.fill(self.color_light)
                    surf.blit(square, (col_index * SQUARESIZE, row_index * SQUARESIZE))
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


    def move_piece(self, piece : Piece, new_row : int, new_col : int):
        """
        move_piece(self, piece: Piece, new_row : int, new_col : int):
        moves the piece on the boards data  structure.
        updates the pieces row and column attributes. 
        Then calls the draw piece instance method to draw the piece onto the board
        returns : None
        """
        
        # Update piece parameters
        old_row = piece.row
        old_col = piece.col
        piece.row = new_row
        piece.col = new_col
        # Update board parameters
        self.struct[old_row][old_col] = None
        self.struct[new_row][new_col] = piece
        
        # draw piece onto new position 
        self.draw_piece(piece, piece.row, piece.col)
        # clear from previous position
        self.clear_piece(piece, old_row, old_col)



        # put new position
        # update piece attributes

        # draw the piece onto board

    def grid_to_rel_pos(self, row : int, col : int) -> tuple:
        """
        grid_to_rel_pos(self, row : int, col : int) -> tuple:
        converts the grid coordinates into a position relative to the board
        returns : a tuple (x,y)
        """
        return (col * SQUARESIZE, row * SQUARESIZE)

    def draw_piece(self, piece : Piece, row : int, col : int):
        """
        draw_piece(self, piece : Piece, row : int , col : int):
        Draws the piece onto the board. 
        returns : None
        """
        pos = self.grid_to_rel_pos(row, col)
        self.surface.blit(piece.surface, pos)

    def clear_piece(self, piece : Piece, row : int, col : int):
        """
        clear_piece(self, piece : Piece):
        Clears the piece from the board. "Undrawing" it 
        returns : None
        """
        pos = self.grid_to_rel_pos(row, col)
        if (row + col) % 2 == 0:
            self.color_square(self.color_dark, row, col)
        else:
            self.color_square(self.color_light, row, col)


    def color_square(self, color : pygame.Color,  row : int, col : int):
        """
        color_square(self, color : pygame.Color,  row : int, col : int):

        Colors the square based on the inputted color, given a row and column on the board.
        creates a pygames surface, fills it with provided color and then blits it onto the board
        surface. 
        returns : None 
        """
        square = pygame.Surface((SQUARESIZE, SQUARESIZE))
        square.fill(color)
        self.surface.blit(square, (col * SQUARESIZE, row * SQUARESIZE))
         

    def draw_board(self, window : pygame.Surface) -> None:
        """
        draw_board(self, window : pygame.Surface):
        Draws the board onto the pygame surface object called window. 
        Blits the board onto the window
        returns : None
        """
        window.blit(self.surface, (BOARDPOSX, BOARDPOSY))

    #def move_piece(self, piece : Piece, pos : list):
