#performs algorithms
import Constants as c
import Library as l

doneNodes = False

def solveAStep(grid):
	global doneNodes
	forwardPredict(grid)
	updatePairs(grid)
	updateColors(grid)
	doneNodes = True

# If any tile has only one possibility left, apply it
def updatePairs(grid):
	for tile in l.expandGrid(grid):
		checkMe(tile)
		if len(tile.directionPairs) == 1:
			tile.directions = tile.directionPairs.pop()

# Fly through all the tiles and make sure they're all the right color.
def updateColors(grid):
	for tile in l.expandGrid(grid):
		if tile.isNode:
			for p in getAllInPath(tile):
				p.number = tile.number

# Run the checks that remove the possibilities
def checkMe(tile):
	if not isDecided(tile):
		# Remove possibilities using Imaginary Corner Back-Propogation
		for pair in diagonalRemove(tile):
			if pair in tile.directionPairs:
				tile.directionPairs.remove(pair)

		adjacents = l.getAdjacentsWithDirections(tile)
		for adj in adjacents:
			if adj[0] is None:
				# We can't go into a wall
				changePairs(tile, adj[1], False)
			else:
				# We can't merge with the head of another color
				if tile.number != 0 and adj[0].number != 0 and adj[0].number != tile.number:
					changePairs(tile, adj[1], False)

				# If something is pointing into me, I have to be pointing back
				if isPointing(adj[0], l.getOpposite(adj[1])):
					changePairs(tile, adj[1], True)
					if adj[0].number != 0 and not tile.isNode:
						tile.number = adj[0].number

					# Remove all squares
					for direc in get90s(adj[1]):
						if isPointing(adj[0], direc):
							changePairs(tile, direc, False)
					
				# Block walls
				if not isPointing(adj[0], l.getOpposite(adj[1])) and isDecided(adj[0]):
					changePairs(tile, adj[1], False)

				# Special node-code since they've 
				if tile.isNode and adj[0].isNode:
					if adj[0].number != tile.number:
						changePairs(tile, adj[1], False)

# This entire algorithm is essentially cheating, since it's glancing into the future. If this algorithm was recursive it would solve the entire thing
# It would also be exponential complexity, which we're trying to avoid.
def forwardPredict(grid):
	for tile in l.expandGrid(grid):
		if not isDecided(tile) and len([x for x in l.getAdjacents(tile) if x is not None and (isDecided(x) or (x.isNode and not doneNodes))]) > 0:
			newPairs = []
			for pair in tile.directionPairs:
				tile.directions = pair
				adjacents = l.getAdjacentsWithDirections(tile)
				validPair = True
				for adj in adjacents:
					if adj[0] is not None and not isDecided(adj[0]):
						backupPairs = list(adj[0].directionPairs)
						backupNumber = adj[0].number
						checkMe(adj[0])
						if len(adj[0].directionPairs) == 0:
							validPair = False
						adj[0].directionPairs = backupPairs
						adj[0].number = backupNumber
				tile.directions = [c.D.u, c.D.u]
				if validPair:
					newPairs.append(pair)
			tile.directionPairs = newPairs

def diagonalRemove(tile):
	toReturn = []
	for p in c.allDirectionPairs:
		if p == c.P.lEW or p == c.P.lNS:
			continue
		if diagonalWall(tile, p):
			toReturn.append(p)
	return toReturn

def diagonalWall(tile, direc):
	if tile.isNode:
		return False

	for d in direc:
		nextTo = l.getNextTo(tile, *d)
		if nextTo is None:
			return True
		if isDecided(nextTo):
			if not isPointing(nextTo, l.getOpposite(d)):
				return True

	nextTile = l.getNextTo(l.getNextTo(tile, *direc[0]), *direc[1])

	if nextTile is None:
		return True

	return diagonalWall(nextTile, direc)

def get90s(direc):
	map = {	c.D.n: (c.D.e, c.D.w),
			c.D.e: (c.D.n, c.D.s),
			c.D.s: (c.D.e, c.D.w),
			c.D.w: (c.D.n, c.D.s)
		}

	return map[direc]

def isDecided(tile):
	return tile.directions[0] != c.D.u or tile.directions[1] != c.D.u

def changePairs(tile, direc, pointingInto):
	newPairs = []
	for pair in tile.directionPairs:
		pointing = False
		for direction in pair:
			if direction == direc:
				pointing = True

		if pointing == pointingInto:
			newPairs.append(pair)
	tile.directionPairs = newPairs

def isPossiblyPointing(tile, direc):
	for p in tile.directionPairs:
		for d in p:
			if d == direc:
				return True

	if isPointing(tile, direc):
		return True

	return False

def isPointing(tile, direc):
	for d in tile.directions:
		if d == direc:
			return True
	return False
	
def addHeads(grid):
	for tile in l.expandGrid(grid):
		for d in tile.directions:
			nextTo = l.getNextTo(tile, *d)
			if nextTo is not None and l.getOpposite(d) not in nextTo.directions:
				l.addDirection(nextTo, l.getOpposite(d))

def isHead(tile):
	for d in tile.directions:
		nextTo = l.getNextTo(tile, *d)
		if nextTo is not None and l.getOpposite(d) not in nextTo.directions:
			return True
	return False

def getAllInPath(n1):
	all = [n1]

	if not isDecided(n1):
		return []

	if isHead(n1):
		return all
	
	for d in n1.directions:
		if d != c.D.u:
			all.extend(getAllInPathFromDirection(n1, l.getNextTo(n1, *d), []))
	return all

def getAllInPathFromDirection(tileBefore, tile, currentStack):
	currentStack.append(tile)
	if not isHead(tile) and not tile.isNode:
		newTile = l.getNextTo(tile, *tile.directions[0])
		if newTile == tileBefore:
			newTile = l.getNextTo(tile, *tile.directions[1])
		getAllInPathFromDirection(tile, newTile, currentStack)
	return currentStack
