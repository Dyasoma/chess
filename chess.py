
# Example file showing a basic pygame "game loop"
import pygame, sys
from pygame.locals import *
WINDOWWIDTH = 800
WINDOWHEIGHT = 800
WINDOWTOBOARDRATIO = 0.8
SQUARECOUNT = 8
BOARDSIDELENGTH = WINDOWWIDTH * WINDOWTOBOARDRATIO
SQUARESIZE = BOARDSIDELENGTH / SQUARECOUNT
BOARDPOSX = (WINDOWWIDTH - BOARDSIDELENGTH) / 2
BOARDPOSY = (WINDOWHEIGHT - BOARDSIDELENGTH) / 2
FPS = 30
BROWN = (185,122,87)
RED = (102, 0, 0)


#Classes
class Square:
    def __init__(
        self, size: int, color: pygame.Color, row: int, col: int
    ):  # row/col are indices
        """
        Square objects represent a single square tile on the board.
        Note that the square in the ith row and jth column will have a position
        (j * size, i * size) where i and j are the indices of the square on the board struct.
        ex: for square in board.struct[3][4] with size 100 it will have a position = (400, 300)
        where the position refers to the top left corner of the square.
        """
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
        self.valid_move = False

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

    def fill_square(self, piece):
        """
        fill_square(self, piece):
        sets the instance attribute "contents" to be filled with a certain piece.
        """
        self.contents = piece

class Board:
    """
    Represents an 8x8 chess board.
    """

    def __init__(self, width: int, height: int, square_count = 8):
        """
        Board is initalized by providing its width and length, and the square_count
        Note that square_count refers to the count of squares along either the x axis or y axis.
        ex: if square count is 5, it will be assumed that a 5x5 board is desired.
        """
        self.width: int = width
        self.height: int = height
        self.square_count: int = square_count
        self.struct = self.__create_board_struct()
        self.surface = self.__create_board_surface()
        self.rect = self.__create_board_rect()
        self.square_size = self.struct[0][0].size
        self.state = 0

    def __create_board_struct(self) -> list[list[Square]]:
        """
        Creates the instance attribute "struct" for the board object of class Board. instance
        attribute refers to the boards Data structure, implemented as a list of lists
        whose entries are objects of class Square. Mutates the list as the list is built.
        board.struct[i][j] refers to the ith row, and the jth column of the board.
        Returns : a list of lists
        Side effect : creates instance attribute "struct" and mutates it
        Calls to create_board_struct will overide previous instance attribute.
        creates empty list,
        """
        struct: list = []
        square_size = self.height / self.square_count
        for row_index in range(self.square_count):
            row = []
            for col_index in range(self.square_count):
                # checks if square is even or odd, setting even to white and odd to black
                if (row_index + col_index) % 2 == 0:
                    color = RED
                else:
                    color = BROWN
                square = Square(square_size, color, row_index, col_index)
                row.append(
                    square
                )  # creates a square and adds it to the struct
            struct.append(row)
        return struct

    def __create_board_surface(self) -> pygame.Surface:
        """
        create_board_surface(self):
        creates the board surface, using the pygame Surface object class, and assigning the returned
        surface as an instance attribute of the board object.
        Serves as the "image" of the board
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

def main():
    screen = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption("Chess")

    # Setup and Initialization
    pygame.init()
    game_is_running = True
    FPSCLOCK = pygame.time.Clock()
    #Chess pieces

    chessboard = Board(BOARDSIDELENGTH, BOARDSIDELENGTH)
    while game_is_running:
        
        # Inputs
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        
        #UPDATE

        # RENDER
        screen.blit(chessboard.surface, chessboard.rect)
        pygame.display.update()
        FPSCLOCK.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
