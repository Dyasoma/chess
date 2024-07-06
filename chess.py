# Example file showing a basic pygame "game loop"
import sys
import pygame
from pygame.locals import *

WINDOWWIDTH = 800
WINDOWHEIGHT = 800
WINDOWTOBOARDRATIO = 1
SQUARECOUNT = 8
BOARDSIDELENGTH = WINDOWWIDTH * WINDOWTOBOARDRATIO
SQUARESIZE = int(BOARDSIDELENGTH / SQUARECOUNT)
BOARDPOSX = (WINDOWWIDTH - BOARDSIDELENGTH) / 2
BOARDPOSY = (WINDOWHEIGHT - BOARDSIDELENGTH) / 2
FPS = 30
DARKRED = (102, 0, 0)
LIGHTBROWN = (185, 122, 87)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


# Classes


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
        self.rel_pos = (
            col * size,
            row * size,
        )  # columns go left to right, rows go up and down
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


class Board:
    """
    Represents an nxn checkered board.
    """
    def __init__(
        self,
        width: int,
        height: int,
        square_count,
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
                # checks if square is even or odd, setting even to white and odd to black
                if (row_index + col_index) % 2 == 0:
                    color = self.color_dark
                else:
                    color = self.color_light
                square = Square(square_size, color, row_index, col_index)
                row.append(square)  # creates a square and adds it to the struct
            struct.append(row)
        return struct

    def __create_board_surface(self) -> pygame.Surface:
        """
        create_board_surface(self):
        creates the board surface, using the pygame Surface object class, and assigning the returned
        surface as an instance attribute of the board object.
        Serves as the "image" of the board
        Board begins "blank" i.e black, blits for a given location the corresponding square.
        Returns : pygame Surface object
        """
        # Surf is first the entire size of the board
        surf = pygame.Surface((self.width, self.height))
        # we go through the board and for each square, we "blit" onto the board the current square.
        for row_index in range(self.square_count):
            for col_index in range(self.square_count):
                current_square: Square = self.struct[row_index][col_index]
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


def main():
    screen = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption("Chess")
    screen.fill("White")

    # Setup and Initialization
    pygame.init()
    game_is_running = True
    clock = pygame.time.Clock()
    mouse_down = False
    # Chess pieces
    pawn = Pawn(SQUARESIZE, WHITE)

    chessboard = Board(BOARDSIDELENGTH, BOARDSIDELENGTH, SQUARECOUNT, DARKRED, LIGHTBROWN)
    while game_is_running:


        # poll for events
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                mouse_down = True
            if event.type == MOUSEBUTTONUP:
                mouse_up = True

        

        # UPDATE

        #if mouse_down and pawn.selected():

        # RENDER
        chessboard.surface.blit(pawn.surface, pawn.rect)
        screen.blit(chessboard.surface, chessboard.rect)
        pygame.display.update()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
