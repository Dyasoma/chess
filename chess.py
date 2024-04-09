
# Example file showing a basic pygame "game loop"
import pygame
import math
WINDOWHEIGHT = 768
WINDOWWIDTH = 768
BOARDSIZE = WINDOWHEIGHT * 2 / 3
PLAYAREASTARTPOSITIONY = (WINDOWHEIGHT / 2) - (BOARDSIZE / 2)
PLAYAREASTARTPOSITIONX = (WINDOWWIDTH / 2) - (BOARDSIZE / 2)
PIECESIZE = [math.floor(BOARDSIZE / 8) , math.floor(BOARDSIZE / 8)]
pieces_size = PIECESIZE[0]
# Setup and Initialization
pygame.init()
game_window = pygame.display.set_mode((WINDOWHEIGHT, WINDOWWIDTH))
clock = pygame.time.Clock()
game_is_running = True
chessboard_surface = pygame.image.load("chessboarddown.png")
chessboard_surface = pygame.transform.scale(chessboard_surface, size=(BOARDSIZE, BOARDSIZE))

chessboard_x_position = WINDOWWIDTH / 2  - BOARDSIZE / 2 
chessboard_y_position = WINDOWHEIGHT / 2  - BOARDSIZE / 2 



# Board data type
chessboard_data = {'a': list(range(1,9)),'b': list(range(1,9)),'c': list(range(1,9)),'d': list(range(1,9)),'e': list(range(1,9)),'f': list(range(1,9)),'g': list(range(1,9))}
chessboard_data


#Chess pieces
# Black
king_black = pygame.image.load("King_black.png")
king_black = pygame.transform.scale(king_black, size=PIECESIZE)
queen_black = pygame.image.load("queen_black.png")
queen_black = pygame.transform.scale(queen_black, size=PIECESIZE)
rook_black_1 = pygame.image.load("rook_black.png")
rook_black_1 = pygame.transform.scale(rook_black_1, size=PIECESIZE)
rook_black_2 = rook_black_1
bishop_black_1 = pygame.image.load("bishop_black.png")
bishop_black_1 = pygame.transform.scale(bishop_black_1, size=PIECESIZE)
bishop_black_2 = bishop_black_1
knight_black_1 = pygame.image.load("knight_black.png")
knight_black_1 = pygame.transform.scale(knight_black_1, size=PIECESIZE)
knight_black_2 = knight_black_1
pawn_black_1 = pygame.image.load("pawn_black.png")
pawn_black_1 = pygame.transform.scale(pawn_black_1, size=PIECESIZE)
pawn_black_2 = pawn_black_1
pawn_black_3 = pawn_black_1
pawn_black_4 = pawn_black_1
pawn_black_5 = pawn_black_1
pawn_black_6 = pawn_black_1
pawn_black_7 = pawn_black_1
pawn_black_8 = pawn_black_1


king_white = pygame.image.load("King_white.png")
king_white = pygame.transform.scale(king_white, size=PIECESIZE)
queen_white = pygame.image.load("queen_white.png")
queen_white = pygame.transform.scale(queen_white, size=PIECESIZE)
rook_white_1 = pygame.image.load("rook_white.png")
rook_white_1 = pygame.transform.scale(rook_white_1, size=PIECESIZE)
rook_white_2 = rook_white_1
bishop_white_1 = pygame.image.load("bishop_white.png")
bishop_white_1 = pygame.transform.scale(bishop_white_1, size=PIECESIZE)
bishop_white_2 = bishop_white_1
knight_white_1 = pygame.image.load("knight_white.png")
knight_white_1 = pygame.transform.scale(knight_white_1, size=PIECESIZE)
knight_white_2 = knight_white_1
pawn_white_1 = pygame.image.load("pawn_white.png")
pawn_white_1 = pygame.transform.scale(pawn_white_1, size=PIECESIZE)
pawn_white_2 = pawn_white_1
pawn_white_3 = pawn_white_1
pawn_white_4 = pawn_white_1
pawn_white_5 = pawn_white_1
pawn_white_6 = pawn_white_1
pawn_white_7 = pawn_white_1
pawn_white_8 = pawn_white_1



x, y = pygame.mouse.get_pos()
while game_is_running:
    
    # Inputs


    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_is_running = False
        #if event.type == pygame.MOUSEBUTTONDOWN:
        if pygame.mouse.get_pressed()[0]:
            x, y = pygame.mouse.get_pos()

    

    #UPDATE


    

    # fill the screen with a color to wipe away anything from last frame
    game_window.fill([0, 0, 0])

    
    

    # RENDER
    # RENDER YOUR GAME HERE
    # flip() the display to put your work on screen
    game_window.blit(chessboard_surface, dest=(WINDOWWIDTH/2 -chessboard_surface.get_width()/2, WINDOWHEIGHT/2 -chessboard_surface.get_height()/2))
    #game_window.blit(queen_black,dest=(x - queen_black.get_height()/2, y - queen_black.get_width()/2))
    game_window.blit(knight_black_1, dest = (PLAYAREASTARTPOSITIONX + pieces_size * 1, PLAYAREASTARTPOSITIONY + pieces_size * 0  ))
    game_window.blit(knight_black_2, dest = (PLAYAREASTARTPOSITIONX + pieces_size * 6, PLAYAREASTARTPOSITIONY + pieces_size * 0  ))
    game_window.blit(rook_black_1, dest = (PLAYAREASTARTPOSITIONX + pieces_size * 0, PLAYAREASTARTPOSITIONY + pieces_size * 0  ))
    game_window.blit(rook_black_2, dest = (PLAYAREASTARTPOSITIONX + pieces_size * 7, PLAYAREASTARTPOSITIONY + pieces_size * 0  ))
    game_window.blit(bishop_black_1, dest = (PLAYAREASTARTPOSITIONX + pieces_size * 2, PLAYAREASTARTPOSITIONY + pieces_size * 0  ))
    game_window.blit(bishop_black_2, dest = (PLAYAREASTARTPOSITIONX + pieces_size * 5, PLAYAREASTARTPOSITIONY + pieces_size * 0  ))
    game_window.blit(queen_black, dest = (PLAYAREASTARTPOSITIONX + pieces_size * 3, PLAYAREASTARTPOSITIONY + pieces_size * 0  ))
    game_window.blit(king_black, dest = (PLAYAREASTARTPOSITIONX + pieces_size * 4, PLAYAREASTARTPOSITIONY + pieces_size * 0  ))
    game_window.blit(pawn_black_1, dest = (PLAYAREASTARTPOSITIONX + pieces_size * 0, PLAYAREASTARTPOSITIONY + pieces_size * 1 ))
    game_window.blit(pawn_black_2, dest = (PLAYAREASTARTPOSITIONX + pieces_size * 1, PLAYAREASTARTPOSITIONY + pieces_size * 1 ))
    game_window.blit(pawn_black_3, dest = (PLAYAREASTARTPOSITIONX + pieces_size * 2, PLAYAREASTARTPOSITIONY + pieces_size * 1 ))
    game_window.blit(pawn_black_4, dest = (PLAYAREASTARTPOSITIONX + pieces_size * 3, PLAYAREASTARTPOSITIONY + pieces_size * 1 ))
    game_window.blit(pawn_black_5, dest = (PLAYAREASTARTPOSITIONX + pieces_size * 4, PLAYAREASTARTPOSITIONY + pieces_size * 1 ))
    game_window.blit(pawn_black_6, dest = (PLAYAREASTARTPOSITIONX + pieces_size * 5, PLAYAREASTARTPOSITIONY + pieces_size * 1 ))
    game_window.blit(pawn_black_7, dest = (PLAYAREASTARTPOSITIONX + pieces_size * 6, PLAYAREASTARTPOSITIONY + pieces_size * 1 ))
    game_window.blit(pawn_black_8, dest = (PLAYAREASTARTPOSITIONX + pieces_size * 7, PLAYAREASTARTPOSITIONY + pieces_size * 1 ))



    game_window.blit(knight_white_1, dest = (PLAYAREASTARTPOSITIONX + pieces_size * 1, PLAYAREASTARTPOSITIONY + pieces_size * 7  ))
    game_window.blit(knight_white_2, dest = (PLAYAREASTARTPOSITIONX + pieces_size * 6, PLAYAREASTARTPOSITIONY + pieces_size * 7  ))

    game_window.blit(rook_white_1, dest = (PLAYAREASTARTPOSITIONX + pieces_size * 0, PLAYAREASTARTPOSITIONY + pieces_size * 7  ))
    game_window.blit(rook_white_2, dest = (PLAYAREASTARTPOSITIONX + pieces_size * 7, PLAYAREASTARTPOSITIONY + pieces_size * 7  ))

    game_window.blit(bishop_white_1, dest = (PLAYAREASTARTPOSITIONX + pieces_size * 2, PLAYAREASTARTPOSITIONY + pieces_size * 7  ))
    game_window.blit(bishop_white_2, dest = (PLAYAREASTARTPOSITIONX + pieces_size * 5, PLAYAREASTARTPOSITIONY + pieces_size * 7  ))

    game_window.blit(queen_white, dest = (PLAYAREASTARTPOSITIONX + pieces_size * 3, PLAYAREASTARTPOSITIONY + pieces_size * 7  ))
    game_window.blit(king_white, dest = (PLAYAREASTARTPOSITIONX + pieces_size * 4, PLAYAREASTARTPOSITIONY + pieces_size * 7  ))

    game_window.blit(pawn_white_1, dest = (PLAYAREASTARTPOSITIONX + pieces_size * 0, PLAYAREASTARTPOSITIONY + pieces_size * 6 ))
    game_window.blit(pawn_white_2, dest = (PLAYAREASTARTPOSITIONX + pieces_size * 1, PLAYAREASTARTPOSITIONY + pieces_size * 6 ))
    game_window.blit(pawn_white_3, dest = (PLAYAREASTARTPOSITIONX + pieces_size * 2, PLAYAREASTARTPOSITIONY + pieces_size * 6 ))
    game_window.blit(pawn_white_4, dest = (PLAYAREASTARTPOSITIONX + pieces_size * 3, PLAYAREASTARTPOSITIONY + pieces_size * 6 ))
    game_window.blit(pawn_white_5, dest = (PLAYAREASTARTPOSITIONX + pieces_size * 4, PLAYAREASTARTPOSITIONY + pieces_size * 6 ))
    game_window.blit(pawn_white_6, dest = (PLAYAREASTARTPOSITIONX + pieces_size * 5, PLAYAREASTARTPOSITIONY + pieces_size * 6 ))
    game_window.blit(pawn_white_7, dest = (PLAYAREASTARTPOSITIONX + pieces_size * 6, PLAYAREASTARTPOSITIONY + pieces_size * 6 ))
    game_window.blit(pawn_white_8, dest = (PLAYAREASTARTPOSITIONX + pieces_size * 7, PLAYAREASTARTPOSITIONY + pieces_size * 6 ))


    pygame.display.flip()
    #



    clock.tick(60)  # limits FPS to 60

pygame.quit()