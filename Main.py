import pygame
import Constants as c
import Library as l
import GenerateNew
from random import random, choice, getstate, setstate, seed
import Algorithmate
import colorsys

pygame.init()
myfont = pygame.font.SysFont("monospace", int(c.BOXSIZE/2))
size = [c.BOXSIZE*c.GRIDSIZE, c.BOXSIZE*c.GRIDSIZE]
screen = pygame.display.set_mode(size)
pygame.display.set_caption('My Game')
clock = pygame.time.Clock()

class Tile():
	def __init__(self, x, y):
		self.x = x
		self.y = y
		# If it is a node then only the first direction is ever used
		self.isNode = False
		self.imaginary = False
		self.number = 0
		self.directions = [c.D.u, c.D.u]
		self.grid = []
		self.directionPairs = c.allDirectionPairs

	def resetMe(self):
		self.isNode = False
		self.number = 0
		self.directions = [c.D.u, c.D.u]
		self.directionPairs = list(c.allDirectionPairs)

	def clone(self):
		toReturn = Tile(self.x, self.y)
		toReturn.isNode = self.isNode
		toReturn.number = self.number
		toReturn.grid = self.grid
		toReturn.directionPairs = self.directionPairs
		for i in range(2):
			toReturn.directions[i] = self.directions[i]
		return toReturn

c.solutionGrid = [[Tile(x, y) for y in range(c.GRIDSIZE)] for x in range(c.GRIDSIZE)]
for tile in l.expandGrid(c.solutionGrid):
	tile.grid = c.solutionGrid

# Start the same every time
setstate(eval(open('state.txt').read()))
GenerateNew.generateNew()

showSolution = False
showComputer = False

mouseDragging = False
currentMouseBox = [-1,-1]

def testingFunc():
	#fixSquares()
	GenerateNew.generateNew()
	pass

showTilePossibilityNum = c.SHOW_ALL_TILE_PAIRS

done = False
while done == False:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			done = True
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_r:
				print("Resetting map ...")
				testingFunc()
			if event.key == pygame.K_s:
				print("Toggling showing solution")
				showSolution = not showSolution
			if event.key == pygame.K_SPACE:
				print("Performing algorithm step")
				showComputer = True
				Algorithmate.trysolve()
			if event.key == pygame.K_c:
				print("Toggling showing computer")
				showComputer = not showComputer
			if event.key == pygame.K_LSHIFT:
				print("Toggling tile possibilities")
				showTilePossibilityNum = not showTilePossibilityNum
			if event.key == pygame.K_y:
				print(GenerateNew.lastState)
			if event.key == pygame.K_i:
				GenerateNew.mergeNodes()
			if event.key == pygame.K_1:
				print("Switching solution mode to RICH")
				l.solutionMode = c.S.RICH
			if event.key == pygame.K_2:
				print("Switching solution mode to BAIL")
				l.solutionMode = c.S.BAIL
			if event.key == pygame.K_3:
				print("Switching solution mode to HARR")
				l.solutionMode = c.S.HARR
			if event.key == pygame.K_e:
				if currentMouseBox != [-1,-1]:
					n1 = c.userGrid[currentMouseBox[0]][currentMouseBox[1]]
					n1.directions = [c.D.u, c.D.u]

		if event.type == pygame.MOUSEBUTTONDOWN:
			if event.button == 1:
				mouseDragging = True
				mouseX, mouseY = event.pos
				currentMouseBox = [mouseX//c.BOXSIZE, mouseY//c.BOXSIZE]

		if event.type == pygame.MOUSEBUTTONUP:
			if event.button == 1:
				mouseDragging = False

		if event.type == pygame.MOUSEMOTION:
			if mouseDragging:
				mouseX, mouseY = event.pos
				newMouseBox = [mouseX//c.BOXSIZE, mouseY//c.BOXSIZE]
				if currentMouseBox != newMouseBox:
					n1 = c.userGrid[currentMouseBox[0]][currentMouseBox[1]]
					n2 = c.userGrid[newMouseBox[0]][newMouseBox[1]]

					ab1 = abs(n1.x-n2.x)
					ab2 = abs(n1.y-n2.y)
					if ab1 > 1 or ab2 > 1 or (ab1 == 1 and ab2 == 1):
						continue

					n2.directions = [c.D.u, c.D.u]
					n1.directions[1] = l.getDirectionFromTo(n1,n2)
					n2.directions[0] = l.getDirectionFromTo(n2,n1)
					n2.number = n1.number

				currentMouseBox = newMouseBox


	screen.fill((0,0,0))

	if showSolution:
		grid = c.solutionGrid
	elif showComputer:
		grid = c.computerGrid
	else:
		grid = c.userGrid

	for x, col in enumerate(grid):
		for y, tile in enumerate(col):
			s = c.BOXSIZE
			gt = c.GRIDTHICKNESS
			color = (50,50,50)
			if tile.imaginary:
				color = (127,127,127)
			else:
				color = GenerateNew.colorList[tile.number]

			center = (int((x+0.5)*s), int((y+0.5)*s))
			pygame.draw.rect(screen, (255,255,255), (x*s+(gt/2), y*s+(gt/2), s-gt, s-gt))

			if l.hasDirection(tile):
				pygame.draw.circle(screen, color, center, int(s/8))

				for i in range(2):
					directionBias = (tile.directions[i][0]/2, tile.directions[i][1]/2)
					loc = ((x+0.5+directionBias[0])*s, (y+0.5+directionBias[1])*s)

					pygame.draw.line(screen, color, loc, center, int(s/4))

			if tile.isNode:
				rad = int(s/3)
				pygame.draw.circle(screen, color, center, rad)
				textcolor = (255,255,255) if color[0]+color[1]+color[2]<255 else (0,0,0)
				text = myfont.render(str(tile.number+1), 1, textcolor)
				rect = text.get_rect()
				screen.blit(text, (center[0]-rect.width/2, center[1]-rect.height/2))
			elif l.isHead(tile):
				rad = int(s/3)
				pygame.draw.circle(screen, color, center, int(rad*0.7))
				if (tile.imaginary):
					text = myfont.render("?", 1, (0,0,0))
					rect = text.get_rect()
					screen.blit(text, (center[0]-rect.width/2, center[1]-rect.height/2))
			if c.SHOW_ALL_TILE_NUMS:
				text = myfont.render(str(tile.number), 1, (0,0,0))
				rect = text.get_rect()
				screen.blit(text, (center[0]-rect.width/2, center[1]-rect.height/2))

			if showTilePossibilityNum:#c.SHOW_ALL_TILE_PAIRS:
				text = myfont.render(str(len(tile.directionPairs)), 1, (255,0,0))
				rect = text.get_rect()
				#screen.blit(text, (center[0]-rect.width/2, center[1]-rect.height/2))

				j = 0
				for direc in tile.directionPairs:
					myCenter = (int((x+0.3*(j % 3)+0.2)*s), int((y+0.2+0.3*(j//3))*s))
					j += 1
					pygame.draw.circle(screen, (200, 200, 200), myCenter, int(s/10))
					for i in range(2):
						directionBias = (direc[i][0]/2, direc[i][1]/2)
						loc = (myCenter[0]+directionBias[0]*s*0.15, myCenter[1]+directionBias[1]*s*0.15)

						pygame.draw.line(screen, (100, 100, 100), loc, myCenter, int(s/40))

	pygame.display.update()
	clock.tick(100)

pygame.quit()
