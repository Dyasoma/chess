import pygame

from .constants import WHITE, BLACK, SQUARESIZE

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

    def set(self, init_row, init_col):
        """
        set(self, init_col, init_row):
        sets the pieces original position on the board
        """
        self.row = init_row
        self.col = init_col

    
    def move(self, new_row, new_col):
        """
        move(self, row, col):
        moves the piece by updating its internal parameters
        returns the pieces old location. If the old location data is not
        captured and stored this method will still update positional parameters
        on valid move. 
        i.e. (o_row, o_col) = piece.move(x,y) is just as valid as
        piece.move(x,y) assuming both are valid moves.  
        """
        # move_piece(self, piece, new_row, new_col)
        # first update piece parameters
        if self.valid_move(new_row, new_col, self.row, self.col):
            old_row = self.row
            old_col = self.col
            self.row = new_row
            self.col = new_col
            return (old_row, old_col) 
        else:
            # if not valid move, parameters don't change
            return (self.row, self.col)

    def valid_move(self, new_row, new_col, old_row, old_col):
        # exists purely to be over written by subclasses
        pass 
    
    def get_rel_pos(self) -> tuple:
        """
        get_rel_pos(self) -> tuple:
        determines the position of the piece relative to the board.
        returns : A tuple (x,y) where x,y gives you the distance from the top left corner of the 
        chess board. 
        """
        return (self.col * self.size, self.row * self.size)
    


class Pawn(Piece):
    def __init__(self, color : pygame.Color, row : int, col : int, piece_type : str):
        super().__init__(color, row, col, piece_type)
        self.passant = False
    def valid_move(self, new_row, new_col, old_row, old_col):
        # pawn can move 1 square at a time
        if self.color == BLACK:
            if (new_col == old_col and new_row == old_row + 1):
                return True
            elif (new_col == old_col + 1 and new_row == old_row + 1) and not self.passant:
                self.passant = True
                return True
            elif (new_col == old_col - 1 and new_row == old_row + 1) and not self.passant:
                self.passant = True
                return True
            else:
                return False
        else:
            if (new_col == old_col and new_row == old_row - 1):
                return True
            elif (new_col == old_col + 1 and new_row == old_row - 1) and not self.passant:
                self.passant = True
                return True
            elif (new_col == old_col - 1 and new_row == old_row - 1) and not self.passant:
                self.passant = True
                return True
            else:
                return False
 
class Knight(Piece):
    #def __init__(self, )
       # super().__init__()
    
    def valid_move(self, new_row, new_col, old_row, old_col):
        # pawn can move 1 square at a time
        if self.color == BLACK:
            return (new_col == old_col and new_row == old_row + 1)
        else:
            return (new_col == old_col and new_row == old_row - 1)       
    

    


