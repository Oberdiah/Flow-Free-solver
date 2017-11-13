import pygame
import Constants as c
import Library as l
from GenerateNew import generateNew
from random import random, choice

pygame.init()
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
		self.directions = [c.D.u, c.D.u]

c.grid = [[Tile(x, y) for y in range(c.GRIDSIZE)] for x in range(c.GRIDSIZE)]

generateNew()

done = False
while done == False:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			done = True
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_LEFT:
				pass

	screen.fill((0,0,0))
	
	for x, col in enumerate(c.grid):
		for y, tile in enumerate(col):
			s = c.BOXSIZE
			gt = c.GRIDTHICKNESS
			center = (int((x+0.5)*s), int((y+0.5)*s))
			pygame.draw.rect(screen, (255,255,255), (x*s+(gt/2), y*s+(gt/2), s-gt, s-gt))

			rad = int(s/8)
			if tile.isNode:
				rad = int(s/4)

			pygame.draw.circle(screen, tile.color, center, rad)

			for i in range(2):
				directionBias = (tile.directions[i][0]/2, tile.directions[i][1]/2)
				loc = ((x+0.5+directionBias[0])*s, (y+0.5+directionBias[1])*s)

				pygame.draw.line(screen, tile.color, loc, center, int(s/4))
	


	pygame.display.update()
	clock.tick(20)
 
pygame.quit()