from chess import Board, Square
BOARDPOSX = 20
BOARDPOSY = 20
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

def test_square_creation():
    size = 80
    YELLOW = (255, 255, 0)
    row = 3
    col = 3
    test_square = Square(size, YELLOW, row, col)
    assert test_square.size == size
    assert test_square.color == YELLOW
    assert test_square.row == row
    assert test_square.col == col
        # rel_pos is relative to the board
        # abs_pos is relative to the entire window
    assert test_square.rel_pos == (col * size, row * size) 
    assert test_square.abs_pos == (col * size + BOARDPOSX, row * size + BOARDPOSY)
    assert test_square.contents == None  # squares hold nothing in the beginning
