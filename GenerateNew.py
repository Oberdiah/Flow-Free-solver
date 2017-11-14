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

	nodesNumber = 0
	for tile in l.shuffle(l.expandGrid(c.solutionGrid)):
		if not tile.isNode and tile.directions[1] == c.D.u:
			tile.isNode = True
			colorList.append(l.randomColor())
			doNodeStuff(tile, c.D.w, len(colorList)-1, 0)
			# Make sure that all nodes have their first direction as their output
			tile.directions[0] = tile.directions[1]
			tile.directions[1] = c.D.u

	mergeNodes()
	mergeNodesNew()
	checkForRedo()

	c.computerGrid = l.cloneGrid(c.solutionGrid)
	for tile in l.expandGrid(c.computerGrid):
		tile.directions = [c.D.u, c.D.u]
	c.userGrid = l.cloneGrid(c.computerGrid)

	failureNum = 0

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
						traceConnectionBack(nextTo, ntn1, len(colorList)-1)
						ntn1.isNode = True
						ntn2.isNode = True
						nextTo.isNode = True
						tile.directions[0] = p
						nextTo.directions[1] = l.getOpposite(p)
						nextTo.directions[0] = c.D.u
						break
			
def traceConnectionBack(tileBefore, tile, num):
	tile.color = colorList[num]
	tile.number = num
	if not tile.isNode:
		newTile = l.getNextTo(tile, *tile.directions[0])
		if newTile == tileBefore:
			newTile = l.getNextTo(tile, *tile.directions[1])
		traceConnectionBack(tile, newTile, num)

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

	# Check if we're making squares
	numNear = 0
	for p in c.all3x3Directions:
		nextTo = l.getNextTo(going, *p)
		if nextTo and nextTo.color == head.color:
			numNear += 1
	if numNear > 2:
		return False

	return True