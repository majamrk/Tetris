import random, time, pygame, sys
from pygame.locals import *

FPS = 25
WINDOWWIDTH = 640
WINDOWHEIGHT = 480
BOXSIZE = 20
BOARDWIDTH = 10
BOARDHEGIHT = 23
BLANK = '-'

MOVESIDEWAYSFREQ = 0.15
MOVEDOWNFREQ = 0.1

TOPMARGIN = WINDOWHEIGHT - (BOARDHEGIHT * BOXSIZE) - 3
XMARGIN = int((WINDOWWIDTH - BOARDWIDTH * BOXSIZE) / 6)
YMARGIN = int((WINDOWWIDTH - BOARDWIDTH * BOXSIZE) / 3)

# R G B
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 155, 0)
BLUE = (72, 118, 255)
YELLOW = (255, 255, 0)
RED = (220, 20, 60)
PURPLE = (155, 48, 255)
MAGENTA = (255, 0, 255)
ORANGE = (255, 128, 0)
BEET = (142, 56, 142)

COLORS = (GREEN, BLUE, YELLOW, RED, MAGENTA, ORANGE, BEET)



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
		addTextScreen('Game Over')

def startGame():
	board = getClearBoard()
	lastDropDownTime = time.time()
	lastDropTime = time.time()
	lastMovingSidewaysTime = time.time()
	movingLeft = False
	movingRight = False
	movingDown = False
	score = 0

	level, fallFreq = getLevelAndFallFreq(score)

	fallingPiece = generateNewPiece()
	nextPiece = generateNewPiece()

	while True:
		if fallingPiece == None:
			fallingPiece = nextPiece
			nextPiece = generateNewPiece()
			lastDropTime = time.time()

			if not possiblePosition(board, fallingPiece):
				return

		checkingForQuit()

		for event in pygame.event.get():
			if event.type == KEYUP:
				if event.key == K_p:
					DISPLAYSURF.fill(BGCOLOR)
					addTextScreen('Paused')
					lastDropTime = time.time()
					lastDropDownTime = time.time()
					lastMovingSidewaysTime = time.time()
				elif event.key == K_LEFT:
					movingLeft = False
				elif event.key == K_RIGHT:
					movingRight = False
				elif event.key == K_DOWN:
					movingDown = False

			elif event.type == KEYDOWN:
				if event.key == K_LEFT and possiblePosition(board, fallingPiece, adjX = -1):
					fallingPiece['x'] -= 1
					movingLeft = True
					movingRight = False
					lastMovingSidewaysTime = time.time()

				elif event.key == K_RIGHT and possiblePosition(board, fallingPiece, adjX = 1):
					fallingPiece['x'] += 1
					movingRight = True
					movingLeft = False
					lastMovingSidewaysTime = time.time()

				elif event.key == K_UP:
					fallingPiece['rotation'] = (fallingPiece['rotation'] + 1) % len(SHAPES[fallingPiece['shape']])
					if not possiblePosition(board, fallingPiece):
						fallingPiece['rotation'] = (fallingPiece['rotation'] - 1) % len(SHAPES[fallingPiece['shape']])

				elif event.key == K_SPACE:
					movingDown = False
					movingLeft = False
					movingRight = False
					for i in range(1, BOARDHEGIHT):
						if not possiblePosition(board, fallingPiece, adjY = i):
							break
					fallingPiece['y'] += i - 1

		if (movingRight or movingLeft) and time.time() - lastMovingSidewaysTime > MOVESIDEWAYSFREQ:
			if movingRight and possiblePosition(board, fallingPiece, adjX = 1):
				fallingPiece['x'] += 1
			elif movingLeft and possiblePosition(board, fallingPiece, adjX = -1):
				fallingPiece['x'] -= 1
			lastMovingSidewaysTime = time.time()



		if time.time() - lastDropTime > fallFreq:
			if not possiblePosition(board, fallingPiece, adjY = 1):
				drawOnBoard(board, fallingPiece)
				score += eraseCompletedLines(board)
				level, fallFreq = getLevelAndFallFreq(score)
				fallingPiece = None
			else:
				fallingPiece['y'] += 1
				lastDropTime = time.time()
			

					

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
				'y': 0,
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

def getLevelAndFallFreq(score):
	level = int(score / 15) + 1
	fallFreq = 0.25 - (level * 0.02)
	return level, fallFreq

def createTextObjects(text, font, color):
	surf = font.render(text, True, color)
	return surf, surf.get_rect()

def addTextScreen(text):
	titleSurf, titleRect = createTextObjects(text, BIGFONT, TEXTCOLOR)
	titleRect.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2) - 5)
	DISPLAYSURF.blit(titleSurf, titleRect)

	while chekingForKeyPress() == None:
		pygame.display.update()
		FPSCLOCK.tick()

def chekingForKeyPress():
	checkingForQuit()

	for event in pygame.event.get([KEYDOWN, KEYUP]):
		if event.type == KEYDOWN:
			continue
		return event.key
	return None

def pieceOnBoard(x, y):
	return x >= 0 and x < BOARDWIDTH and y < BOARDHEGIHT

def possiblePosition(board, piece, adjX = 0, adjY = 0):
	for x in range(TEMPLATEWIDTH):
		for y in range(TEMPLATEHIGHT):
			overBoard = y + piece['y'] + adjY < 0
			if overBoard or SHAPES[piece['shape']][piece['rotation']][y][x] == BLANK:
				continue
			if not pieceOnBoard(x + piece['x'] + adjX, y + piece['y'] + adjY):
				return False
			if board[x + piece['x'] + adjX][y + piece['y'] + adjY] != BLANK:
				return False
	return True


def drawOnBoard(board, piece):
	for x in range(TEMPLATEWIDTH):
		for y in range(TEMPLATEHIGHT):
			if SHAPES[piece['shape']][piece['rotation']][y][x] != BLANK:
				board[x + piece['x']][y + piece['y']] = piece['color']


def completedLine(board, y):
	for x in range(BOARDWIDTH):
		if board[x][y] == BLANK:
			return False
	return True

def eraseCompletedLines(board):
	linesRemoved = 0
	y = BOARDHEGIHT - 1
	while y >= 0:
		if completedLine(board, y):
			for drawDownY in range(y, 0, -1):
				for x in range(BOARDWIDTH):
					board[x][drawDownY] = board[x][drawDownY - 1]
			linesRemoved += 1

		else:
			y -= 1	
	return linesRemoved	


if __name__ == '__main__':
	main()