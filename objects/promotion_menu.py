from .constants import (
    BOARDPOSX,
    BOARDPOSY,
    BOARDSIDELENGTH,
    SQUARESIZE,
    BLACK,
    GREY,
    WHITE,
)
import pygame


class PromotionMenu:
    """
    Represents a simplisitic promotion menu used to upgrade pawns

    Args:
        color (pygame.Color): The color of the piece that will be upgraded, i.e. Team color

    Attributes:
        image_options (list[str]): A list containing strings for which piece a pawn can upgrade into and the color
        options (list[str]): A list containing strings for which a piece a pawn can upgrade into, no colors
        w (int): The width of the menu relative to the board it is drawn on
        h (int): The height of the menu relative to the board it is drawn on
        x (int): The horizontal pixel position of the board relative to the top left corner of the board
        y (int): The vertical pixel position of the board relative to the top left corner of the board
        surface (pygame.Surface): The image of the board
        rect (pygame.Rect): Position and size of the board
    """

    def __init__(self, color: pygame.Color):
        self.color: pygame.Color = color
        self.image_options: list[str] = self._build_img_options()
        self.w: int = len(self.image_options) * SQUARESIZE
        self.h: int = SQUARESIZE
        self.y: int = 0.5 * BOARDSIDELENGTH - 0.5 * self.h
        self.x: int = 0.5 * BOARDSIDELENGTH - 0.5 * self.w
        self.surface: pygame.Surface = pygame.Surface((self.w, self.h))
        self.rect: pygame.Rect = self.surface.get_rect(topleft=(self.x, self.y))
        self._draw_base_surface()

    def _build_img_options(self) -> list[str]:
        """
        Builds a list used for image options

        each element has form "type_color"

        Returns:
            list[str]: A list whose elements are strings containing a piece and color,
            used as part of a file path.

        """
        options = []
        if self.color == BLACK:
            color_str = "black"
        elif self.color == WHITE:
            color_str = "white"
        else:
            raise TypeError(f"Invalid Color : {self.color}")

        piece_types = ["rook", "bishop", "knight", "queen"]
        options = []
        for piece in piece_types:
            options.append(f"{piece}_{color_str}")
        return options

    def valid_promotion_selected(self, mouse_pos: tuple[int, int]) -> int | None:
        """
        Checks if a valid promotion was selected, and if so returns the selected option as an index value that corresponds
        with the values available in the self.img_options attribute

        Args:
            mouse_pos tuple[int, int]: The mouse position relative to the game window

        Returns:
            int | None: Returns an integer if a valid option was selected, otherwise None. 
        """
        mouse_x, mouse_y = mouse_pos
        local_x = mouse_x - BOARDPOSX
        local_y = mouse_y - BOARDPOSY
        if not self.rect.collidepoint(local_x, local_y):
            return None
        
        offset_x = mouse_x - (BOARDPOSX + self.x)
        #selection = int((mouse_x - self.x) // SQUARESIZE)
        selection = int((offset_x) // SQUARESIZE)
        count = len(self.image_options)
        if 0 <= selection < count:
            return selection
        else:
            return None

    def _draw_base_surface(self):
        """
        Creates the basic surface of the promotion menu. 

        Assumes that the self.surface attribute and the corrersponding image file paths exist
        """
        # we go through the board and for each square, we "blit" onto the board the current square.
        options_count = len(self.image_options)
        for i in range(options_count):
            square = pygame.Surface((SQUARESIZE, SQUARESIZE))
            square.fill(GREY)
            img = pygame.image.load(f"./Assets/{self.image_options[i]}.png")
            img = pygame.transform.smoothscale(img, (SQUARESIZE, SQUARESIZE))
            square.blit(img, (0, 0))
            self.surface.blit(square, (i * SQUARESIZE, 0))
