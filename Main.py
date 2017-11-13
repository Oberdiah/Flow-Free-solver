import pygame
import Constants
from random import random, choice

pygame.init()
size = [Constants.BOXSIZE*Constants.GRIDSIZE, Constants.BOXSIZE*Constants.GRIDSIZE]
screen = pygame.display.set_mode(size)
pygame.display.set_caption('My Game')
clock = pygame.time.Clock()

# Essentially a directions Enum
class D():
	n = (0,1)
	s = (0,-1)
	e = (1,0)
	w = (-1,0)
	u = (0,0)

allDirections = [D.n, D.s, D.e, D.w]

class Tile():
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.color = (int(random()*255), int(random()*255), int(random()*255))
		self.directions = [choice(allDirections), choice(allDirections)]

grid = [[Tile(x, y) for x in range(Constants.GRIDSIZE)] for y in range(Constants.GRIDSIZE)]

done = False
while done == False:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			done = True

	screen.fill((0,0,0))
	
	for x, col in enumerate(grid):
		for y, tile in enumerate(col):
			s = Constants.BOXSIZE
			gt = Constants.GRIDTHICKNESS
			center = (int((x+0.5)*s), int((y+0.5)*s))
			pygame.draw.rect(screen, (255,255,255), (x*s+(gt/2), y*s+(gt/2), s-gt, s-gt))

			pygame.draw.circle(screen, tile.color, center, int(s/8))

			for i in range(2):
				directionBias = (tile.directions[i][0]/2, tile.directions[i][1]/2)
				loc = ((x+0.5+directionBias[0])*s, (y+0.5+directionBias[1])*s)

				pygame.draw.line(screen, tile.color, loc, center, int(s/4))
	
	pygame.display.update()
	clock.tick(20)
 
pygame.quit()