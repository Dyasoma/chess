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
    def __init__(self, color):
        self.color = color
        self.image_options = self.__build_img_options()
        self.options = self.__build_options()
        self.options_count = len(self.image_options)
        self.w = len(self.options) * SQUARESIZE
        self.h = SQUARESIZE
        self.y =  0.5 * BOARDSIDELENGTH - 0.5 * self.h
        self.x =  0.5 * BOARDSIDELENGTH - 0.5 * self.w
        self.surface: pygame.Surface = pygame.Surface((self.w, self.h))
        self.rect: pygame.Rect = self.surface.get_rect(topleft=(self.x, self.y))
        self.__draw_base_surface()

    def __build_img_options(self):
        options = []
        color_str = "white"
        if self.color == BLACK:
            color_str = "black"
            options.append(f"rook_{color_str}")
            options.append(f"bishop_{color_str}")
            options.append(f"knight_{color_str}")
            options.append(f"queen_{color_str}")
        elif self.color == WHITE:
            options.append(f"rook_{color_str}")
            options.append(f"bishop_{color_str}")
            options.append(f"knight_{color_str}")
            options.append(f"queen_{color_str}")
        return options
    
    def __build_options(self):
        options = []
        options.append(f"rook")
        options.append(f"bishop")
        options.append(f"knight")
        options.append(f"queen")
        return options

    def valid_promotion_selected(self, mouse_pos):
        mouse_x = mouse_pos[0]
        mouse_y = mouse_pos[1]
        if not self.rect.collidepoint(mouse_x - BOARDPOSX, mouse_y - BOARDPOSY):
            return None
        else:
            option = int((mouse_x - self.x) // SQUARESIZE)
            if 0 <= option < 4:
                return option
            else:
                return None

    def __draw_base_surface(self):
        # we go through the board and for each square, we "blit" onto the board the current square.

        for i in range(self.options_count):
            square = pygame.Surface((SQUARESIZE, SQUARESIZE))
            square.fill(GREY)
            img = pygame.image.load(f"./Assets/{self.image_options[i]}.png")
            img = pygame.transform.smoothscale(img, (SQUARESIZE, SQUARESIZE))
            square.blit(img, (0, 0))
            self.surface.blit(square, (i * SQUARESIZE, 0))
