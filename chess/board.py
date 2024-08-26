import pygame
from .constants import BOARDPOSX, BOARDPOSY
from .square import Square


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


    def __create_board_struct(self) -> list[list[Square]]:
        """
        Creates the instance attribute "struct" for the board object of class Board.
        refers to the boards data structure, implemented as a list of lists
        whose entries are objects of class Square. Mutates the list as the list is built.
        board.struct[i][j] refers to the ith row, and the jth column of the board.
        Returns : a list of lists
        Side effect : creates instance attribute "struct" and mutates it
        """
        struct: list = []
        square_size = self.height / self.square_count
        for row_index in range(self.square_count):
            row = []
            for col_index in range(self.square_count):
                color = (0, 0, 0)
                square = Square(square_size, color, row_index, col_index)
                row.append(square)  # creates a square and adds it to the struct
            struct.append(row)
        return struct

    def __create_board_surface(self) -> pygame.Surface:
        """
        create_board_surface(self):
        creates the board surface, using the pygame Surface object class, and assigning the returned
        surface as an instance attribute of the board object.
        Creates a black surface.
        Sets each squares color instance attribute.
        blits square from struct attribute onto surface attribute.
        Serves as the "image" of the board.
        Returns : pygame Surface object
        """
        # Surf is first the entire size of the board
        surf = pygame.Surface((self.width, self.height))
        # we go through the board and for each square, we "blit" onto the board the current square.
        for row_index in range(self.square_count):
            for col_index in range(self.square_count):
                current_square: Square = self.struct[row_index][col_index]
                # checks if square is even or odd, setting even to white and odd to black
                if (row_index + col_index) % 2 == 0:
                    current_square.update_color(self.color_dark)
                else:
                    current_square.update_color(self.color_light)
                surf.blit(current_square.surface, current_square.rel_pos)
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
    
    def draw_board(self, window : pygame.Surface) -> None:
        """
        draw_board(self, window : pygame.Surface):
        Draws the board onto the pygame surface object called window. 
        Blits the board onto the window
        returns : None
        """
        window.blit(self.surface, (BOARDPOSX, BOARDPOSY))