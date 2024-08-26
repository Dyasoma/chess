import pygame
from .constants import WHITE, SQUARESIZE

class Piece:
    def __init__(self, color, piece_type : str):
        self.size = SQUARESIZE
        self.piece_type = piece_type
        self.color = color
        self.surface = self.__create_piece_surface()
        self.rect = self.__create_piece_rect()

    def __create_piece_surface(self) -> pygame.Surface:
        """
        __create_piece_surface(self) -> pygame.Surface:
        Creates the surface instance attribute for the given piece
        First loading an image depending on the piece type
        Then scales the image
        returns : pygame surface object for the image of the piece
        """
        # creates the surface for which transparency is allowed
        #surf = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        #surf.fill((0, 0, 0, 0))   # fills surface with "transparent" color.
        #return surf
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
        return self.surface.get_rect()
    


