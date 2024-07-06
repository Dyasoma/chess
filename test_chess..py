from chess import * 
import numpy

def similar_surfaces(surface_1 : pygame.Surface, surface_2 : pygame.Surface):
    cond_1 = str(surface_1.get_view()) == str(surface_2.get_view())
    cond_2 = surface_1.get_rect() == surface_2.get_rect()
    cond_3 = surface_1.get_bytesize() == surface_2.get_bytesize()
    cond_4 = surface_1.get_offset() == surface_2.get_offset()
    cond_5 = surface_1.get_parent() == surface_2.get_parent()
    return cond_1 and cond_2 and cond_3 and cond_4 and cond_5

def equal_surfaces(surface_1 : pygame.Surface, surface_2 : pygame.Surface):
    array_1 = pygame.surfarray.array2d(surface_1)
    array_2 = pygame.surfarray.array2d(surface_2)
    return numpy.array_equal(array_1, array_2)    
    

def equal_rects(rect_1 : pygame.Rect, rect_2 : pygame.Rect):
    cond_1 = rect_1.size == rect_2.size
    cond_2 = rect_1.center == rect_2.center 
    cond_3_half = rect_1.top == rect_2.top and rect_1.bottom == rect_2.bottom
    cond_3 = cond_3_half and rect_1.left == rect_2.left and rect_1.right == rect_2.right
    return  cond_1 and cond_2 and cond_3



def test_board_creation():
    width = 500
    height = 500
    square_count = 8
    color_dark = (255, 0, 255)
    color_light = (0, 255, 0)
    test_board = Board(500, 500, 8, (255,0,255), (0, 255, 0))

    assert test_board.width == width
    assert test_board.height == height
    assert test_board.color_light == color_light
    assert test_board.color_dark ==  color_dark
    assert test_board.square_count ==  square_count
    assert test_board.surface.get_size() == (width, height)
    assert similar_surfaces(test_board.surface, pygame.Surface((width, height)))
    assert equal_rects(test_board.rect, pygame.Surface((width, height)).get_rect())

def test_square_creation():
    size = 80
    YELLOW = (255, 255, 0)
    row = 3
    col = 3
    test_square = Square(size, YELLOW, row, col)
    ref_surface = pygame.Surface((size, size))
    ref_surface.fill(YELLOW)
    assert test_square.size == size
    assert test_square.color == YELLOW
    assert test_square.row == row
    assert test_square.col == col
        # rel_pos is relative to the board
        # abs_pos is relative to the entire window
    assert test_square.rel_pos == (col * size, row * size)
    assert test_square.abs_pos == (col * size + BOARDPOSX, row * size + BOARDPOSY)
    assert test_square.contents == None  # squares hold nothing in the beginning
    assert test_square.surface.get_size() == (size,size)
    assert equal_surfaces(test_square.surface, ref_surface)
    assert equal_rects(test_square.rect, ref_surface.get_rect(topleft = test_square.abs_pos))

