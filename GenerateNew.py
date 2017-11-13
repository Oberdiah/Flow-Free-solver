import Constants as c
from random import random, choice, randint
import Library as l

def generateNew():
	for tile in l.shuffle(l.expandGrid()):
		if not tile.isNode and tile.directions[1] == c.D.u:
			tile.isNode = True
			doNodeStuff(tile, c.D.w, l.randomColor(), 0)
			# Make sure that all nodes have their first direction as their output
			tile.directions[0] = tile.directions[1]
			tile.directions[1] = c.D.u

	for tile in l.expandGrid():
		if tile.isNode and tile.directions[0] == c.D.u and tile.directions[1] == c.D.u:
			for p in c.allDirections:
				nextTo = l.getNextTo(tile, *p)
				if nextTo and nextTo.isNode:
					tile.color = nextTo.color
					if nextTo.directions[0] != c.D.u or nextTo.directions[1] != c.D.u:
						nextTo.isNode = False
					tile.directions[0] = p
					nextTo.directions[1] = l.getOpposite(p)
					break



def doNodeStuff(me, dIn, color, length):
	x = me.x
	y = me.y

	me.color = color

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
	# Check if we've been there before
	if not going or going.isNode or going.directions[1] != c.D.u:
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