import Constants as c
from random import random, choice, randint
import Library as l

def generateNew():
	for tile in l.shuffle(l.expandGrid()):
		if not tile.isNode and tile.directions[1] == c.D.u:
			tile.isNode = True
			doNodeStuff(tile, c.D.w, l.randomColor(), 0)

def doNodeStuff(me, dIn, color, length):
	x = me.x
	y = me.y

	me.color = color

	if random() < c.NODEFRACTION and length > 2:
		me.isNode = True
		return

	possibleDirections = list(c.allDirections)
	possibleDirections.extend([dIn]*c.STRAIGHTNESS)
	possibleDirections = l.shuffle(possibleDirections)
	for d in possibleDirections:
		# Check if we just came from there
		if d == l.getOpposite(dIn):
			continue

		# Check if we've been there before
		going = l.getNextTo(me, d[0], d[1])
		if not going or going.isNode or going.directions[1] != c.D.u:
			continue

		# Check if we're making squares
		numNear = 0
		for p in c.all3x3Directions:
			nextTo = l.getNextTo(going, *p)
			if nextTo and nextTo.color == me.color:
				numNear += 1
		if numNear > 3:
			continue

		me.directions[1] = d
		going.directions[0] = l.getOpposite(d)
		doNodeStuff(going, d, color, length+1)

		return

	me.isNode = True



#	for x, col in enumerate(grid):
#		for y, tile in enumerate(col):
