import pygame
from .constants import WHITE

class Pawn:
    def __init__(self, size, color):
        self.size = size
        self.color = color
        self.surface = self.__create_piece_surface()
        self.rect = self.__create_piece_rect()

    def __create_piece_surface(self) -> pygame.Surface:
        """
        """
        # creates the surface for which transparency is allowed
        #surf = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        #surf.fill((0, 0, 0, 0))   # fills surface with "transparent" color.
        #return surf
        if self.color == WHITE:
            surface = pygame.image.load("pawn_white.png")
        else:
            surface = pygame.image.load("pawn_black.png")
        return pygame.transform.smoothscale(surface, (self.size, self.size))

    def __create_piece_rect(self) -> pygame.Rect:
        """

        """
        return self.surface.get_rect()
    

    #def selected(mouse_position):
        #if 

