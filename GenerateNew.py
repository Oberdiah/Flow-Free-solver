import Constants as c
from random import random, choice, randint
import Library as l

colorList = []
failureNum = 0

def generateNew():
	global failureNum
	for tile in l.expandGrid(c.solutionGrid):
		tile.resetMe()
	colorList.clear()
	
	createPaths()
	mergeNodes()
	mergeNodesNew()
	mergePaths()
	checkForRedo()

	c.computerGrid = l.cloneGrid(c.solutionGrid)
	for tile in l.expandGrid(c.computerGrid):
		tile.directions = [c.D.u, c.D.u]
		if not tile.isNode:
			tile.color = l.randomColor()
			tile.number = -1
	c.userGrid = l.cloneGrid(c.computerGrid)

	failureNum = 0

def mergePaths():
	for tile in l.expandGrid(c.solutionGrid):
		if tile.isNode:
			for d in c.allDirections:
				nextTo = l.getNextTo(tile, *d)
				if nextTo and nextTo.isNode and nextTo.number != tile.number:
					goodToGo = True
					fullPath = l.getAllInPath(nextTo)
					for p in fullPath:
						numNear = numberNear(p, nextTo.number) + numberNear(p, tile.number)
						if numNear > 2:
							goodToGo = False

					if goodToGo:
						nextTo.isNode = False
						tile.isNode = False
						l.createBond(nextTo, tile)
						for p in fullPath:
							p.color = tile.color
							p.number = tile.number
						break
							
def numberNear(tile, number):
	numNear = 0
	for q in c.all3x3Directions:
		nextTo = l.getNextTo(tile, *q)
		if nextTo and nextTo.number == number:
			numNear += 1
	return numNear

def createPaths():
	nodesNumber = 0
	for tile in l.shuffle(l.expandGrid(c.solutionGrid)):
		if not tile.isNode and tile.directions[1] == c.D.u:
			tile.isNode = True
			colorList.append(l.randomColor())
			doNodeStuff(tile, choice(c.allDirections), len(colorList)-1, 0)
			# Make sure that all nodes have their first direction as their output
			tile.directions[0] = tile.directions[1]
			tile.directions[1] = c.D.u

def mergeNodesNew():
	for tile in l.expandGrid(c.solutionGrid):
		if tile.isNode and l.hasNoDirection(tile):
			for p in c.allDirections:
				nextTo = l.getNextTo(tile, *p)
				if nextTo:
					ntn1 = l.getNextTo(nextTo, *nextTo.directions[0])
					ntn2 = l.getNextTo(nextTo, *nextTo.directions[1])
					if not nextTo.isNode and not ntn1.isNode and not ntn2.isNode:
						nextTo.color = tile.color
						nextTo.number = tile.number
						l.breakBond(nextTo, ntn1)
						l.breakBond(nextTo, ntn2)
						colorList.append(l.randomColor())
						for q in l.getAllInPath(ntn1):
							num = len(colorList)-1
							q.color = colorList[num]
							q.number = num
						ntn1.isNode = True
						ntn2.isNode = True
						nextTo.isNode = True
						tile.directions[0] = p
						nextTo.directions[1] = l.getOpposite(p)
						nextTo.directions[0] = c.D.u
						break

def mergeNodes():
	# Merge all single nodes
	for tile in l.expandGrid(c.solutionGrid):
		if tile.isNode and tile.directions[0] == c.D.u and tile.directions[1] == c.D.u:
			for p in c.allDirections:
				nextTo = l.getNextTo(tile, *p)
				if nextTo and nextTo.isNode and validExtension(nextTo, tile):
					tile.color = nextTo.color
					tile.number = nextTo.number
					if nextTo.directions[0] != c.D.u or nextTo.directions[1] != c.D.u:
						nextTo.isNode = False
					tile.directions[0] = p
					nextTo.directions[1] = l.getOpposite(p)
					break


def checkForRedo():
	global failureNum
	for tile in l.expandGrid(c.solutionGrid):
		if tile.isNode and tile.directions[0] == c.D.u and tile.directions[1] == c.D.u:
			failureNum += 1
			print("Single found at {}, {}. Regenerating map. This is attempt {}".format(tile.x, tile.y, failureNum))
			generateNew()
			break


def doNodeStuff(me, dIn, color, length):
	x = me.x
	y = me.y

	me.color = colorList[color]
	me.number = color

	if random() < c.SNAKEENDCHANCE and length > c.MINIMUMSNAKELENGTH:
		me.isNode = True
		return

	possibleDirections = list(c.allDirections)
	possibleDirections.extend([dIn]*c.STRAIGHTNESS)
	possibleDirections = l.shuffle(possibleDirections)
	for d in possibleDirections:
		# Check if we just came from there
		if d == l.getOpposite(dIn):
			continue

		going = l.getNextTo(me, d[0], d[1])
		if not validExtension(me, going):
			continue

		me.directions[1] = d
		going.directions[0] = l.getOpposite(d)
		doNodeStuff(going, d, color, length+1)

		return

	me.isNode = True

def validExtension(head, going):
	if not going:
		return False

	# Check if we've been there before
	if l.hasDirection(going):
		return False

	if not l.isColorValid(going, head.number):
		return False

	return True