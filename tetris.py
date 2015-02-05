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

COLORS = (GREEN, BLUE, YELLOW, RED, MAGENTA, ORANGE, BEET)
#beet_box = pygame.image.load('beet_box.png')
#blue_box = pygame.image.load('blue_box.png')
#green_box = pygame.image.load('green_box.png')
#magenta_box = pygame.image.load('magenta_box.png')
#orange_box = pygame.image.load('orange_box.png')
#red_box = pygame.image.load('red_box.png')
#yellow_box = pygame.image.load('yellow_box.png')


TEMPLATEHIGHT = 4
TEMPLATEWIDTH = 4


L_ROTATIONS = [['----',
				'-000',
			    '-0--',
		    	'----'],
			   ['--0-',
				'--0-',
				'--00',
				'----'],
			   ['---0',
				'-000',
				'----',
				'----'],
			   ['-00-',
				'--0-',
				'--0-',
				'----']]

O_ROTATIONS = [['----',
				'-00-',
				'-00-',
				'----']]
				
				  
Z_ROTATIONS = [['----',
				'-00-',
				'--00',
				'----'],
			   ['---0',
				'--00',
				'--0-',
				'----']]


J_ROTATIONS = [['----',
				'-000',
				'---0',
				'----'],
			   ['--00',
				'--0-',
				'--0-',
				'----'],
			   ['-0--',
				'-000',
				'----',
				'----'],
			   ['--0-',
				'--0-',
				'-00-',
				'----']]

S_ROTATIONS = [['----',
				'--00',
				'-00-',
				'----'],
			   ['--0-',
				'--00',
				'---0',
				'----']]


I_ROTATIONS = [['----',
				'0000',
				'----',
				'----'],
			   ['--0-',
				'--0-',
				'--0-',
				'--0-']]
				

T_ROTATIONS = [['----',
				'-000',
				'--0-',
				'----'],
			   ['--0-',
				'--00',
				'--0-',
				'----'],
			   ['--0-',
				'-000',
				'----',
				'----'],
			   ['--0-',
				'-00-',
				'--0-',
				'----']]


SHAPES = {'L': L_ROTATIONS,
		'O': O_ROTATIONS,
		'Z': Z_ROTATIONS,
		'J': J_ROTATIONS,
		'S': S_ROTATIONS,
		'I': I_ROTATIONS,
		'T': T_ROTATIONS}


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
	fallingPiece = generateNewPiece()
	nextPiece = generateNewPiece()

	while True:
		checkingForQuit()
		DISPLAYSURF.fill(BGCOLOR)
		drawingBoard(board)
		addStatus(level, score)
		addNextPiece(nextPiece)
		if fallingPiece != None:
			addPiece(fallingPiece)
		
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

	for x in range(BOARDWIDTH):
		for y in range(BOARDHEGIHT):
			addSquare(x, y, board[x][y])


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

def addSquare(boxx, boxy, color, pixelx = None, pixely = None):
	if color == BLANK:
		return
	if pixelx == None and pixely == None:
		pixelx, pixely = convertToPixelCoords(boxx, boxy)

	pygame.draw.rect(DISPLAYSURF, COLORS[color], (pixelx + 1, pixely + 1, BOXSIZE - 1, BOXSIZE - 1))

def generateNewPiece():
	shape = random.choice(list(SHAPES.keys()))
	newPiece = {'shape': shape,
				'rotation': random.randint(0, len(SHAPES[shape]) - 1),
				'x': int(BOARDWIDTH / 2) - int(TEMPLATEWIDTH / 2),
				'y': -4,
				'color': random.randint(0, len(COLORS) - 1)}
	return newPiece


def convertToPixelCoords(boxx, boxy):
	return (XMARGIN + (boxx * BOXSIZE)), (TOPMARGIN + (boxy * BOXSIZE))

def addPiece(piece, pixelx = None, pixely = None):
	shapeToDraw = SHAPES[piece['shape']][piece['rotation']]
	if pixelx == None and pixely == None:
		pixelx, pixely = convertToPixelCoords(piece['x'], piece['y'])

	for x in range(TEMPLATEWIDTH):
		for y in range(TEMPLATEHIGHT):
			if shapeToDraw[y][x] != BLANK:
				addSquare(None, None, piece['color'], pixelx + (x * BOXSIZE), pixely + (y * BOXSIZE))
				

def addNextPiece(piece):
	nextSurf = BASICFONT.render('Next: ', True, TEXTCOLOR)
	nextRect = nextSurf.get_rect()
	nextRect.topleft = (WINDOWWIDTH - 220, 350)
	DISPLAYSURF.blit(nextSurf, nextRect)

	addPiece(piece, pixelx = WINDOWWIDTH - 230, pixely = 380)


if __name__ == '__main__':
	main()