import Constants as c
from random import random, sample

def shuffle(lst):
	return sample(lst, len(lst))

def expandGrid():
	tiles = []
	for x, col in enumerate(c.grid):
		for y, tile in enumerate(col):
			tiles.append(tile)

	return tiles

def getOpposite(d):
	map = { c.D.e: c.D.w,
			c.D.w: c.D.e,
			c.D.s: c.D.n,
			c.D.n: c.D.s,
			#D.u: D.u
		   }

	return map[d]

def getNextTo(tile, x, y):
	gx = tile.x + x
	gy = tile.y + y

	# Check if we're still on the board
	if gx >= c.GRIDSIZE or gy >= c.GRIDSIZE or gx < 0 or gy < 0:
		return None

	return c.grid[gx][gy]

def randomColor():
	return (int(random()*255), int(random()*255), int(random()*255))
		
