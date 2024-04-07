
# Example file showing a basic pygame "game loop"
import pygame
WINDOWHEIGHT = 768
WINDOWWIDTH = 768
# Setup and Initialization
pygame.init()
game_window = pygame.display.set_mode((WINDOWHEIGHT, WINDOWWIDTH))
clock = pygame.time.Clock()
game_is_running = True
chessboard_surface = pygame.image.load("chessboarddown.png")
chessboard_surface = pygame.transform.scale(chessboard_surface, size=(512,512))

chessboard_x_position = WINDOWWIDTH / 2  - 512 / 2 
chessboard_y_position = WINDOWHEIGHT / 2  - 512 / 2 



# Board data type
chessboard_data = {'a': list(range(1,9)),'b': list(range(1,9)),'c': list(range(1,9)),'d': list(range(1,9)),'e': list(range(1,9)),'f': list(range(1,9)),'g': list(range(1,9))}
chessboard_data


#Chess pieces

king_black = pygame.image.load("King_black.png")
king_black = pygame.transform.scale(king_black, size=(62,62))


queen_black = pygame.image.load("queen_black.png")
queen_black = pygame.transform.scale(queen_black, size=(62,62))

rook_black = pygame.image.load("rook_black.png")
rook_black = pygame.transform.scale(rook_black, size=(62,62))

bishop_black = pygame.image.load("bishop_black.png")
bishop_black = pygame.transform.scale(bishop_black, size=(62,62))

knight_black_1 = pygame.image.load("knight_black.png")
knight_black_1 = pygame.transform.scale(knight_black_1, size=(62,62))
knight_black_2 = knight_black_1
game_window.blit(knight_black_1,dest=(0 - knight_black_1.get_height()/2 * 3 , 0 - knight_black_1.get_width()/2 * 3))


pawn_black = pygame.image.load("pawn_black.png")
pawn_black = pygame.transform.scale(pawn_black, size=(62,62))

pawn_black_1 = pawn_black
pawn_black_2 = pawn_black
pawn_black_3 = pawn_black
pawn_black_4 = pawn_black
pawn_black_5 = pawn_black
pawn_black_6 = pawn_black
pawn_black_7 = pawn_black
pawn_black_8 = pawn_black





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
    game_window.blit(knight_black_1, dest = (512/8 * 7  + chessboard_x_position, 512/8 * 7 + chessboard_y_position))
    pygame.display.flip()
    #



    clock.tick(60)  # limits FPS to 60

pygame.quit()