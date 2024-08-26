import pygame
from .constants import WHITE, SQUARESIZE

class Piece:
    def __init__(self, color : pygame.Color, row : int, col : int, piece_type : str):
        """
        Class used to represent a chess piece.
        """
        self.size = SQUARESIZE
        self.piece_type = piece_type
        self.row = row
        self.col = col
        # first index is the row, second is the col
        self.color = color
        self.surface = self.__create_piece_surface()
        self.rel_pos = self.get_rel_pos()
        self.rect = self.__create_piece_rect()

    def __create_piece_surface(self) -> pygame.Surface:
        """
        __create_piece_surface(self) -> pygame.Surface:
        Creates the surface instance attribute for the given piece
        First loading an image depending on the piece type
        Then scales the image
        returns : pygame surface object for the image of the piece
        """
        if self.color == WHITE: 
            surface = pygame.image.load(f"chess\Assets\{self.piece_type}_white.png")
        else:
            surface = pygame.image.load(f"chess\Assets\{self.piece_type}_black.png")
        return pygame.transform.smoothscale(surface, (self.size, self.size))

    def __create_piece_rect(self) -> pygame.Rect:
        """
        __create_piece_rect(self) -> pygame.Rect:
        creates a pygame rect object for the instance attribute rect
        returns : a pygame rect object
        """
        return self.surface.get_rect(topleft = (self.rel_pos))
    
    def get_rel_pos(self) -> tuple:
        """
        get_rel_pos(self) -> tuple:
        determines the position of the piece relative to the board.
        returns : A tuple (x,y) where x,y gives you the distance from the top left corner of the 
        chess board. 
        """
        return (self.col * self.size, self.row * self.size)
    


    

    


