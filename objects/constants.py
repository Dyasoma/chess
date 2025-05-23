import pygame

WINDOWWIDTH = 1600
WINDOWHEIGHT = 1600
WINDOWTOBOARDRATIO = 1
SQUARECOUNT = 8
BOARDSIDELENGTH = WINDOWWIDTH * WINDOWTOBOARDRATIO
SQUARESIZE = int(BOARDSIDELENGTH / SQUARECOUNT)
BOARDPOSX = (WINDOWWIDTH - BOARDSIDELENGTH) / 2
BOARDPOSY = (WINDOWHEIGHT - BOARDSIDELENGTH) / 2
EMPTY = None
# COLORS
DARKCOLOR = (102, 0, 0)
LIGHTCOLOR = (185, 122, 87)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
GOLD = (255, 215, 0)
GREY = (119, 136, 153)
SELECTPIECE = 0
SELECTMOVE = 1
SELECTPROMOTION = 2
BLACKPLAYER = 0
WHITEPLAYER = 1
