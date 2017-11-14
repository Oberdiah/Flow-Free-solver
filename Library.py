import Constants as c
from random import random, sample

def shuffle(lst):
	return sample(lst, len(lst))

def cloneGrid(grid):
	newGrid = []
	for x, col in enumerate(grid):
		newGrid.append([])
		for y, tile in enumerate(col):
			newGrid[x][y] = tile.clone()
	return newGrid

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
			c.D.u: c.D.u
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

def breakBond(n1, n2):
	for (i1, d1) in enumerate(n1.directions):
		for (i2, d2) in enumerate(n2.directions):
			if d1 == getOpposite(d2) and getNextTo(n1, *d1) == n2 and getNextTo(n2, *d2) == n1 :
				n1.directions[i1] = n2.directions[i2] = c.D.u

def addDirection(n1, d1):
	for d in n1.directions:
		if d == c.D.u:
			d = d1
			return

	assert False, "There was no free direction to add"
		
