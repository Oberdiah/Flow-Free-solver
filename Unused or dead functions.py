
		
def fixSquares():
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
					if n.isNode and l.getOpposite(d) in n.directions:
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