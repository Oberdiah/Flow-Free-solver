import pygame
import Constants as c
import Library as l
import GenerateNew
from random import random, choice

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
		# Should only be used for printing
		self.number = -1
		self.directions = [c.D.u, c.D.u]

	def resetMe(self):
		self.isNode = False
		self.color = l.randomColor()
		self.number = -1
		self.directions = [c.D.u, c.D.u]
		self.userDirections = [c.D.u, c.D.u]

	def clone(self):
		toReturn = Tile(self.x, self.y)
		toReturn.isNode = self.isNode
		toReturn.color = self.color
		for i in range(2):
			toReturn.directions[i] = self.directions[i]
		return toReturn

c.grid = [[Tile(x, y) for y in range(c.GRIDSIZE)] for x in range(c.GRIDSIZE)]
GenerateNew.generateNew()

showSolution = False

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
				showSolution = not showSolution

	screen.fill((0,0,0))
	
	for x, col in enumerate(c.grid):
		for y, tile in enumerate(col):
			s = c.BOXSIZE
			gt = c.GRIDTHICKNESS
			center = (int((x+0.5)*s), int((y+0.5)*s))
			pygame.draw.rect(screen, (255,255,255), (x*s+(gt/2), y*s+(gt/2), s-gt, s-gt))

			if showSolution:
				directions = tile.directions
			else:
				directions = tile.userDirections

			if directions[0] != c.D.u or directions[1] != c.D.u:
				pygame.draw.circle(screen, tile.color, center, int(s/8))

				for i in range(2):
					directionBias = (directions[i][0]/2, directions[i][1]/2)
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