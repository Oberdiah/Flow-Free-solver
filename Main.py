import pygame
import Constants as c
import Library as l
import GenerateNew
from random import random, choice
import Algorithmate

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
		self.color = l.randomColor()
		# The number is always unique, whereas the color has a very small chance of being duplicated
		self.number = -1
		self.directions = [c.D.u, c.D.u]
		self.grid = []

	def resetMe(self):
		self.isNode = False
		self.color = l.randomColor()
		self.number = -1
		self.directions = [c.D.u, c.D.u]

	def clone(self):
		toReturn = Tile(self.x, self.y)
		toReturn.isNode = self.isNode
		toReturn.color = self.color
		toReturn.number = self.number
		toReturn.grid = self.grid
		for i in range(2):
			toReturn.directions[i] = self.directions[i]
		return toReturn

c.solutionGrid = [[Tile(x, y) for y in range(c.GRIDSIZE)] for x in range(c.GRIDSIZE)]
for tile in l.expandGrid(c.solutionGrid):
	tile.grid = c.solutionGrid

GenerateNew.generateNew()

showSolution = False
showComputer = False

def testingFunc():
	#fixSquares()
	GenerateNew.generateNew()
	pass

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
			center = (int((x+0.5)*s), int((y+0.5)*s))
			pygame.draw.rect(screen, (255,255,255), (x*s+(gt/2), y*s+(gt/2), s-gt, s-gt))

			if l.hasDirection(tile):
				pygame.draw.circle(screen, tile.color, center, int(s/8))

				for i in range(2):
					directionBias = (tile.directions[i][0]/2, tile.directions[i][1]/2)
					loc = ((x+0.5+directionBias[0])*s, (y+0.5+directionBias[1])*s)

					pygame.draw.line(screen, tile.color, loc, center, int(s/4))

			if tile.isNode:
				rad = int(s/3)
				pygame.draw.circle(screen, tile.color, center, rad)
				text = myfont.render(str(tile.number+1), 1, (0,0,0))
				rect = text.get_rect()
				screen.blit(text, (center[0]-rect.width/2, center[1]-rect.height/2))

	pygame.display.update()
	clock.tick(20)

pygame.quit()
