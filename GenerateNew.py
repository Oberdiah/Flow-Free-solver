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

	sortErrors()

def sortErrors():
	# Merge all single nodes
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
		
	# Fix squares
	for n1 in l.expandGrid():
		co = n1.color
		n2 = l.getNextTo(n1, 0, 1)
		n3 = l.getNextTo(n1, 1, 0)
		n4 = l.getNextTo(n1, 1, 1)
		newColor = l.randomColor()
		if n2 and n3 and n4 and n2.color == co and n3.color == co and n4.color == co:
			if n1.isNode + n2.isNode + n3.isNode + n4.isNode == 1:
				breakageMap = { (n1, c.D.e): (n2,n4),
								(n1, c.D.s): (n3,n4),
								(n2, c.D.w): (n1,n3),
								(n2, c.D.s): (n3,n4),
								(n3, c.D.e): (n2,n4),
								(n3, c.D.n): (n1,n2),
								(n4, c.D.n): (n1,n2),
								(n4, c.D.w): (n1,n3),
								}
				colorMap =    { (n1, c.D.e): (n1,n2),
								(n1, c.D.s): (n1,n3),
								(n2, c.D.w): (n1,n2),
								(n2, c.D.s): (n2,n4),
								(n3, c.D.e): (n3,n4),
								(n3, c.D.n): (n1,n3),
								(n4, c.D.n): (n2,n4),
								(n4, c.D.w): (n3,n4),
								}

				for (n, d) in breakageMap:
					if n.isNode and d in n.directions:
						br1, br2 = breakageMap[(n, d)]
						br1.isNode = True
						br2.isNode = True
						breakBond(br1,br2)

						co1, co2 = colorMap[(n, d)]
						co1.color = newColor
						co2.color = newColor
						break
			else:
				
				breakageMap = { (n1,n2): (n3,n4),
								(n2,n4): (n1,n3),
								(n3,n4): (n1,n2),
								(n1,n3): (n2,n4)}
				colorMap =    { (n1,n2): (n1,n3),
								(n2,n4): (n1,n2),
								(n3,n4): (n1,n3),
								(n1,n3): (n3,n4)}

				newColor = l.randomColor()
				for (n, p) in breakageMap:
					if n.isNode and p.isNode:
						br1, br2 = breakageMap[(n, p)]
						br1.isNode = True
						br2.isNode = True
						breakBond(br1,br2)

						co1, co2 = colorMap[(n, p)]
						co1.color = newColor
						co2.color = newColor

						break
					
def breakBond(n1, n2):
	for (i1, d1) in enumerate(n1.directions):
		for (i2, d2) in enumerate(n2.directions):
			if d1 == l.getOpposite(d2) and l.getNextTo(n1, *d1) == n2 and l.getNextTo(n2, *d2) == n1 :
				n1.directions[i1] = n2.directions[i2] = c.D.u


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