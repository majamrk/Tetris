import random, time, pygame, sys
from pygame.locals import *

FPS = 25
WINDOWWIDTH = 640
WINDOWHEIGHT = 480
BOXSIZE = 20
BOARDWIDTH = 10
BOARDHEGIHT = 20
BLANK = '-'

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
YELLOW = (255, 255, 0)
RED = (220, 20, 60)
PURPLE = (155, 48, 255)
MAGENTA = (255, 0, 255)
ORANGE = (255, 128, 0)
BEET = (142, 56, 142)

#beet_box = pygame.image.load('beet_box.png')
#blue_box = pygame.image.load('blue_box.png')
#green_box = pygame.image.load('green_box.png')
#magenta_box = pygame.image.load('magenta_box.png')
#orange_box = pygame.image.load('orange_box.png')
#red_box = pygame.image.load('red_box.png')
#yellow_box = pygame.image.load('yellow_box.png')

#shapes.colors = ['beet_box', 'blue_box', 'green_box', 'magenta_box', 'orange_box', 'red_box', 'yellow_box']

#shapes.rotations = {
	
#}


BORDEDCOLOR = PURPLE
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
	board = getClearBoard()
	score = 0
	level = 0
	drawingBoard(board)
	addStatus(level, score)
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


def drawingBoard(board):
	# draw border of the board
	pygame.draw.rect(DISPLAYSURF, BORDEDCOLOR, (XMARGIN - 5, TOPMARGIN - 9, (BOARDWIDTH * BOXSIZE) + 10, (BOARDHEGIHT * BOXSIZE) + 10), 4)

	# draw the background of the board
	pygame.draw.rect(DISPLAYSURF, BGCOLOR, (XMARGIN, TOPMARGIN, BOARDWIDTH * BOXSIZE, BOARDHEGIHT * BOXSIZE))


def addStatus(level, score):
	# drawing level text
	levelSurf = BASICFONT.render('Level: %s' % level, True, TEXTCOLOR)
	levelRect = levelSurf.get_rect()
	levelRect.topleft = (WINDOWWIDTH - 220, 150)
	DISPLAYSURF.blit(levelSurf, levelRect)

	# drawing score text
	scoreSurf = BASICFONT.render('Score: %s' % score, True, TEXTCOLOR)
	scoreRect = scoreSurf.get_rect()
	scoreRect.topleft = (WINDOWWIDTH - 220, 250)
	DISPLAYSURF.blit(scoreSurf,  scoreRect)


def getClearBoard():
	board = []
	for i in range(BOARDWIDTH):
		board.append([BLANK] * BOARDHEGIHT)
	return board


if __name__ == '__main__':
	main()