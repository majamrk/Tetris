import random, time, pygame, sys
from pygame.locals import *

FPS = 25
WINDOWWIDTH = 640
WINDOWHEIGHT = 480
BOXSIZE = 20
BOARDWIDTH = 10
BOARDHEGIHT = 20

MOVESIDEWAYSFREQ = 0.15
MOVEDOWNFREQ = 0.1

TOPMARGIN = WINDOWHEIGHT - (BOARDHEGIHT * BOXSIZE) - 3
XMARGIN = int((WINDOWWIDTH - BOARDWIDTH * BOXSIZE) / 6)
YMARGIN = int((WINDOWWIDTH - BOARDWIDTH * BOXSIZE) / 3)

# R G B
WHITE = (255, 255, 255)
GRAY = (185, 185, 185)
BLACK = (0, 0, 0)
GREEN = (0, 155, 0)
BLUE = (0, 0, 155)
YELLOW = (155, 155, 0)
RED = (155, 0, 0)

BORDEDCOLOR = GREEN
BGCOLOR = BLACK
TEXTCOLOR = WHITE
SHADOWCOLOR = GRAY

def main():
	global FPSCLOCK, DISPLAYSURF, BASICFONT, BIGFONT
	pygame.init()
	FPSCLOCK = pygame.time.Clock()
	DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
	BASICFONT = pygame.font.Font('freesansbold.ttf', 20)
	BIGFONT = pygame.font.Font('freesansbold.ttf', 85)
	pygame.display.set_caption('Tetris vulgaris')

	while True:
		startGame()

def startGame():
	checkingForQuit()
	pygame.display.update()
	FPSCLOCK.tick(FPS)


def checkingForQuit():
	# first get all quit events
	for event in pygame.event.get(QUIT):
		terminate()
	for event in pygame.event.get(KEYUP):
		if event.key == K_ESCAPE:
			terminate()
		pygame.event.post(event)


def terminate():
	pygame.quit()
	sys.exit()


if __name__ == '__main__':
	main()