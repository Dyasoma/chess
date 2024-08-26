import pygame
from .constants import BOARDPOSX, BOARDPOSY


class Square:
    """
    Square objects represent a single square tile on the board.
    Note that the square in the ith row and jth column will have a position
    (j * size, i * size) where i and j are the indices of the square on the board struct.
    ex: for square in board.struct[3][4] with size 100 it will have a position = (400, 300)
    where the position refers to the top left corner of the square.
    """
    def __init__(
        self, size: int, color: pygame.Color, row: int, col: int
    ):  # row/col are indices
     
        self.size = size
        self.color = color
        self.row = row
        self.col = col
        # rel_pos is relative to the board
        # abs_pos is relative to the entire window
        self.rel_pos = (col * size, row * size)
        # columns go left to right, rows go up and down
        self.abs_pos = (col * size + BOARDPOSX, row * size + BOARDPOSY)
        self.surface = self.__create_square_surface()
        self.rect = self.__create_square_rect()
        self.contents = None  # squares hold nothing in the beginning
        

    def __create_square_surface(self) -> pygame.Surface:
        """
        __create_square_surface(self) -> pygame.Surface:
        creates a surface object for the current square, which should be square.
        Fills the square with the given color
        returns : pygame surface object.
        """
        surf = pygame.Surface((self.size, self.size))
        surf.fill(self.color)
        return surf

    def __create_square_rect(self) -> pygame.Rect:
        """
        __create_square_rect(self) -> pygame.Rect:
        creates the rectangular area of the square, If the board does not fill the entire window
        Then rec.x and rec.y are positions relative to the window, not the board.
        returns : pygame rect object
        """
        rec = self.surface.get_rect(topleft=self.abs_pos)
        return rec


    def update_color(self, color : pygame.Color) -> None:
        """
        update_color(self, color : pygame.Color):
        updates the color instance attribute
        Changes the surface to be that color
        returns : None
        """
        self.color = color
        self.surface.fill(self.color)

