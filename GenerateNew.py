import Constants as c
from random import random, choice, randint, getstate, shuffle
import Library as l
import SpecialSolver

colorList = []
failureNum = 0
lastState = 0

tilesToGen = []
nodesPlaced = 0
headList = []
def generateNew():
	#This tries a new method of generating a board,
	#by first filling it with a series of trivial paths
	#As a byproduct, it will more rarely have very long paths going
	#along walls (which is a shame), however it is guaranteed to
	#always be a satisfiable Flow board.
	global failureNum, lastState, colorList, tilesToGen, nodesPlaced

	SpecialSolver.doneNodes = False
	lastState = getstate()

	for tile in l.expandGrid(c.solutionGrid):
		tile.resetMe()
	colorList = [(0,0,0)]
	nodesPlaced = 0
	tilesToGen = []

	tilesToGen = l.expandGrid(c.solutionGrid)
	while fillBoardWithTrivials():
		continue
	while combineBoardTrivials():
		continue
	#[add the combinification code here to make bigger paths]

	c.computerGrid = l.cloneGrid(c.solutionGrid)
	for tile in l.expandGrid(c.computerGrid):
		tile.directions = [c.D.u, c.D.u]
		if not tile.isNode:
			tile.number = 0
		else:
			tile.directionPairs = c.allNodeDirectionPairs
	c.userGrid = l.cloneGrid(c.computerGrid)

	failureNum = 0

def combineBoardTrivials():
	global headList
	didAMerge = False
	for h in headList:
		if h.isNode:
			adjacents = l.getAdjacents(h)
			adjacents = [x for x in adjacents if x is not None]
			adjacents = [x for x in adjacents if x.isNode]
			adjacents = [x for x in adjacents if not l.wouldIntersect_generator(x,h)]
			shuffle(adjacents)
			if len(adjacents)>0:
				didAMerge = True
				thePathToBeShovedIntoThisOne = l.getAllInPath_generator(adjacents[0])
				adjacents[0].isNode = False
				h.isNode = False
				l.createBond(h,adjacents[0])
				for p in thePathToBeShovedIntoThisOne:
					p.number = h.number
	return didAMerge

def fillBoardWithTrivials():
	global nodesPlaced,tilesToGen,headList,colorList
	if (len(tilesToGen)) == 0:
		return False
	tilesum = int(random()*len(tilesToGen)) #Get random tile
	tile = tilesToGen[tilesum]
	tilesToGen.pop(tilesum)
	if l.isEmpty(tile):
		#can put thingamajig here
		adjacents = l.getReachableAdjacents_generation(tile)
		if len(adjacents)>0:
			#simple case, can add new node directly adjacent to it wherever
			tile.isNode = True
			nodesPlaced+=1
			tile.number = nodesPlaced
			tile.imaginary = False
			whichAdj = adjacents[int(random()*len(adjacents))]
			whichAdj.isNode = True
			whichAdj.number = tile.number
			whichAdj.imaginary = False
			colorList.append(l.randomColor())
			headList.append(tile)
			headList.append(whichAdj)
			l.createBond(tile,whichAdj)
		else:
			#This is more complicated - this is a singleton node and cannot move
			#anywhere.  These are illegal, so what we need to do is join it with
			#an adjacent path.
			pathsToJoin = l.getJoinablePaths_generation(tile)
			whichPath = pathsToJoin[int(random()*len(pathsToJoin))]
			adjacents = l.getAdjacents(tile)
			adjacentToMergeTo = [x for x in whichPath if x in adjacents and x.isNode]
			assert len(adjacentToMergeTo)==1,"Two valid merges is contradiction, and zero is preposterous!: "+str(len(adjacentToMergeTo))
			adjacentToMergeTo[0].isNode = False
			tile.isNode = True
			tile.number = adjacentToMergeTo[0].number
			tile.imaginary = False
			headList.append(tile)
			headList.remove(adjacentToMergeTo[0])
			l.createBond(tile,adjacentToMergeTo[0])
		return True
	else:
		#re-run.  This isn't a problem, the random number just landed on a tile that
		#had the counterpart to a generated head on it.  It has now been popped from the list,
		#so no infinite loop shenanigans will happen
		return True

def generateNew_old():
	global failureNum, lastState, colorList

	SpecialSolver.doneNodes = False
	lastState = getstate()

	for tile in l.expandGrid(c.solutionGrid):
		tile.resetMe()
	colorList = [(0,0,0)]

	createPaths()
	mergeNodes()
	mergeNodesNew()
	mergePaths()
	checkForRedo()

	c.computerGrid = l.cloneGrid(c.solutionGrid)
	for tile in l.expandGrid(c.computerGrid):
		tile.directions = [c.D.u, c.D.u]
		if not tile.isNode:
			tile.number = 0
		else:
			tile.directionPairs = c.allNodeDirectionPairs
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
						nextTo.number = tile.number
						l.breakBond(nextTo, ntn1)
						l.breakBond(nextTo, ntn2)
						colorList.append(l.randomColor())
						for q in l.getAllInPath(ntn1):
							num = len(colorList)-1
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


def doNodeStuff(me, dIn, number, length):
	x = me.x
	y = me.y

	me.number = number

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
		doNodeStuff(going, d, number, length+1)

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
