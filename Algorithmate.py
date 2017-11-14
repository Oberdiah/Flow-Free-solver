#performs algorithms
import Constants as c
import Library as l

#Definition of Flow:
#m*n grid of 2L paired nodes ("heads") and m*n-2L empty nodes, with a hole at
#every vertex.
#A solution of Flow is a set of paths between paired nodes such that:
#	1: No paths cross
#	2: Every node belongs to exactly 1 path
#	3: Every path is topologically equivalent to a line
#
#Alternatively, one can restate it as the following:
#
#m*n grid of 2L paired nodes ("heads") and m*n-2L empty nodes.
#A solution of Flow is a set of paths between paired nodes such that:
#	1: No paths cross
#	2: Every node belongs to exactly 1 path
#	3: There is no vertex such that all adjacent nodes belong to the same path
#			(AKA no squares)
#	4: No path forms a closed loop
#
#The first definition is preferred as it is mathematically rigorous
#whereas the second definition contains an ambiguous term 'loop'
#However, the second definition is easier to understand.
#
#The two definitions are provably equivalent:
#
#The definition of a surface being topologically equivalent to a line
#is equivalent to the statement that a surface contains no holes.  If vertices
#are defined as holes, as they are in definition 1, then any square encircles a
#hole and thus breaks topological equivalency, and any loop also breaks
#topological equivalency.  Thus if a path does not satisfy definition 2, it
#fails to satisfy definition 1, and vice versa (as the only situation in which
#a path is not topologically equivalent to a line is when it contains a hole,
#which only happens if either a path encircles a vertex or a larger area).  Thus
#the sets of invalid solutions to both is equivalent, and thus the set of valid
#solutions is equivalent.

#Some definitions (only applies to proofs and may not reflect variable names
#	in the code):
#
#A 'grid' is the board that Flow is played on
#A 'node' is a tile on the grid
#A 'path' is an ordered set of nodes such that no two nodes adjacent in the path
#	are non-adjacent on the grid.
#A 'head' is a node on the end of a path
#	Note that whether a node is or isn't a head can change, depending on how much
#	the player knows about the board:
#	A @ @ @ A, As are heads @s are empty
#   A A @ @ A, All 3 As are heads
#   A A A @ A, All As are heads, but the second one from the left
#   A A A A A, only the leftmost and rightmost As are heads
#A 'wall' is either a node on a path that is not a head, or it is part of the
#	border of the grid.
#A 'square' is any set of 4 nodes with a common vertex all belonging
#to the same path
#A 'loop' is [insert a rigorous definition here]

def trysolve():
	#print(c.grid)
	trytrivials(c.computerGrid)

def trytrivials(grid):
	#This function attempts trivial solves on the grid.
	#A trivial solve is the following:
	#If a head node has 1 adjacency and only 1, it must
	#pass through there.  This is provable:
	#Let H be a head node with one adjacency A.  There must be a path P from H
	#to its corresponding H'.  Let P pass through an adjacency other than A.
	#Then, there is a contradiction, as there is no such adjacency other than A.
	#Thus, A is on path P.

	#grid = l.cloneGrid(grid)
	for row in grid:
		for tile in row:
			adjacents = l.getAdjacentsWithDirections(tile)
			adjacents = [x for x in adjacents if x[0] is not None]#get rid of 'nones'
			#if a tile has at least one unknown direction, it is not an invalid move (assuming it is not a head)
			adjacents = [x for x in adjacents if x[0].directions[0] is c.D.u or x[0].directions[1] is c.D.u]
			#if x is head and it has one known direction, it is an invalid move
			adjacents = [x for x in adjacents if not (x[0].isNode and not l.hasDirection(x[0]))]
			#if adjacents is only size 1, it only has one possible move:
			if len(adjacents) == 1:
				print("Found goodies")
				direc = adjacents[0][1]
				if tile.directions[0]==c.D.u:
					tile.directions[0]=direc
				elif tile.directions[1]==c.D.u:
					tile.directions[1]=direc
				else:
					assert "Error: tile already going EVERYWHERE!  SPLAT."
