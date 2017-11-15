import Constants as c
from random import random, sample

numberOfImaginaryLines = 0

def shuffle(lst):
	return sample(lst, len(lst))

def cloneGrid(grid):
	newGrid = []
	for x, col in enumerate(grid):
		newGrid.append([])
		for y, tile in enumerate(col):
			newGrid[x].append(tile.clone())
			newGrid[x][y].grid = newGrid
	return newGrid

# Turns the 2D array into a 1D array for iterating purposes
def expandGrid(grid):
	tiles = []
	for x, col in enumerate(grid):
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

def hasNoDirection(n1):
	return (n1.directions[0] == c.D.u and n1.directions[1] == c.D.u)

def hasDirection(n1):
	return not hasNoDirection(n1)

def getAllInPath(n1):
	all = [n1]
	if isEmpty(n1):
		return all
	for d in n1.directions:
		if d != c.D.u:
			all.extend(getAllInPathFromDirection(n1, getNextTo(n1, *d), []))
	return all

def getAllInPath_algorithms(n1):
	all = [n1]
	if isEmpty(n1):
		return all
	for d in n1.directions:
		if d != c.D.u:
			all.extend(getAllInPathFromDirection_algorithms(n1, getNextTo(n1, *d), []))
	return all


def getAllInPathFromDirection(tileBefore, tile, currentStack):
	currentStack.append(tile)
	if not tile.isNode:
		newTile = getNextTo(tile, *tile.directions[0])
		if newTile == tileBefore:
			newTile = getNextTo(tile, *tile.directions[1])
		getAllInPathFromDirection(tile, newTile, currentStack)
	return currentStack

def getAllInPathFromDirection_algorithms(tileBefore, tile, currentStack):
	currentStack.append(tile)
	if not isHead(tile):
		newTile = getNextTo(tile, *tile.directions[0])
		if newTile == tileBefore:
			newTile = getNextTo(tile, *tile.directions[1])
		getAllInPathFromDirection_algorithms(tile, newTile, currentStack)
	return currentStack

def getNodeDirection(node):
	for d in node.directions:
		if d != c.D.u:
			return d

def getAdjacents(tile):
	return [getNextTo(tile, *d) for d in c.allDirections]

def getAdjacentsWithDirections(tile):
	return [(getNextTo(tile, *d),d) for d in c.allDirections]

def getNextTo(tile, dx, dy):
	gx = tile.x + dx
	gy = tile.y + dy

	# Check if we're still on the board
	if gx >= c.GRIDSIZE or gy >= c.GRIDSIZE or gx < 0 or gy < 0:
		return None

	return tile.grid[gx][gy]

def randomColor():
	return (int(random()*255), int(random()*255), int(random()*255))

def isColorValid(tile, number):
	# Check if we're making squares
	numNear = 0
	for p in c.all3x3Directions:
		nextTo = getNextTo(tile, *p)
		if nextTo and nextTo.number == number:
			numNear += 1

	if numNear > 2:
		return False
	return True

# Breaks a bond between two adjacent Tiles
def breakBond(n1, n2):
	for (i1, d1) in enumerate(n1.directions):
		for (i2, d2) in enumerate(n2.directions):
			if d1 == getOpposite(d2) and getNextTo(n1, *d1) == n2 and getNextTo(n2, *d2) == n1 :
				n1.directions[i1] = n2.directions[i2] = c.D.u

def createBond(n1, n2):
	addDirection(n1, getDirectionFromTo(n1,n2))
	addDirection(n2, getDirectionFromTo(n2,n1))

def getDirectionFromTo(n1, n2):
	dx = n2.x-n1.x
	dy = n2.y-n1.y
	for d in c.allDirections:
		if d[0] == dx and d[1] == dy:
			return d

	assert False, "Your 'from' and 'to' were more than one apart from one another!"

# Add a new direction onto a Node
def addDirection(n1, d1):
	for i, d in enumerate(n1.directions):
		if d == c.D.u:
			n1.directions[i] = d1
			return

	assert False, "There was no free direction to add"

def hasSingleDirection(tile):
	return (tile.directions[0]==c.D.u and tile.directions[1]!=c.D.u) or (tile.directions[0]!=c.D.u and tile.directions[1]==c.D.u)

def isHead(tile):
	if tile is None:
		return False
	if (tile.imaginary and hasNoDirection(tile)):
		return True
	elif (tile.isNode and hasNoDirection(tile)):
		return True
	elif (not tile.isNode) and hasSingleDirection(tile):
		return True
	return False

def connected(a,b):
	return a in getAllInPath_algorithms(b)

def isWall(tile):
	if tile is None:
		return True
	return not isHead(tile) and not isEmpty(tile)

def isEmpty(tile):
	if tile is None:
		return True
	return tile.number==0

def wouldIntersect(a,b):
	if isEmpty(a) or isEmpty(b):
		return False
	p1 = getAllInPath_algorithms(a)
	p2 = getAllInPath_algorithms(b)
	for n1 in p1:
		for n2 in p2:
			if n2 in [x for x in getAdjacents(n1) if not isEmpty(x)]:
				if not (isHead(n1) and isHead(n2)):
					return True
	return False
