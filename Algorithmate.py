#performs algorithms
import Constants as c
import Library as l
import SpecialSolver

#Definition of Flow:
#m*n grid of 2L paired nodes ("heads") and m*n-2L empty nodes, with a hole at
#every vertex.
#A solution of Flow is a set of paths between paired nodes such that:
#	1: No paths cross eachother or themselves
#	2: Every node belongs to exactly 1 path
#	3: Every path is topologically equivalent to a line
#
#Alternatively, one can restate it as the following:
#
#m*n grid of 2L paired nodes ("heads") and m*n-2L empty nodes.
#A solution of Flow is a set of paths between paired nodes such that:
#	1: No paths cross eachother or themselves
#	2: Every node belongs to exactly 1 path
#	3: There is no vertex such that all adjacent nodes belong to the same path
#			(AKA no squares)
#	4: There is no path P which contains a node N such that N is
#			adjacent to another node on P but neither directly before
#			or after it on the sequence of nodes in P
#			(AKA no loops)
#The first definition is preferred as it is simpler to state mathematically
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
#	are non-adjacent on the grid and there are no repeats.
#A 'head' is a node on the end of a path
#	Note that whether a node is or isn't a head can change, depending on how much
#	the player knows about the board:
#	A @ @ @ A, As are heads @s are empty
#   A A @ @ A, All 3 As are heads
#   A A A @ A, All As are heads, except for the second one from the left
#   A A A A A, only the leftmost and rightmost As are heads
#A 'starting head' is a node that is an endpoint of a path P such that P is in
#	the set of paths that solve the puzzle
#A 'wall' is either a node on a path that is not a head, or it is part of the
#	border of the grid.
#A 'square' is any set of 4 nodes with a common vertex, all belonging
#	to the same path
#A path has a 'loop' if for any node on the path, it is adjacent to
#	another node on the same path, but neither of the nodes follow immediately
#	after the other.

stepByStep = True

def trysolve():
	if l.solutionMode == c.S.BAIL:
		trytrivials(c.computerGrid)
	elif l.solutionMode == c.S.RICH:
		SpecialSolver.solveAStep(c.computerGrid)

def trytrivials(grid):
	Trivial1(grid)
	Trivial2(grid)
	Trivial3(grid)
	Trivial4(grid)

	#This function attempts trivial solves on the grid.
	#"Triviality" means it can be proved by only considerning
	#the direct adjacencies of a node or vertex
	#A trivial solve is one of the following:
	#	Trivial 1:
	#		If a head node has 1 adjacency and only 1, it must
	#		pass through there.
	#		Proof:
	#			Let H be a head node with one adjacency A.  There must be a path P from H
	#			to its corresponding H'.  Let P pass through an adjacency other than A.
	#			Then, there is a contradiction, as there is no such adjacency other than A.
	#			Thus, A is on path P.
	#
	#	Trivial 2:
	#		If 2 same-color heads are adjacent, they must connect
	#		Proof:
	#			If they were not to connect, there would have to be some other
	#			valid path P between them.  However, if that were the case, then
	#			P would completely enclose some region of the board R, as paths
	#			are contiguous and the two heads are next two eachother causing
	#			the ends of the paths to also be adjacent.  Therefore it violates
	#			the condition of topological equivalency to a line.
	#		Alternate Proof:
	#			If they were not to connect, there would have to be some other
	#			valid path P between them.  However, if that were the case, the
	#			starting heads of P would be adjacent but not sequential in P,
	#			thus forming a loop.
	#
	#	Trivial 3:
	#		If an empty node has only 2 adjacencies, it must pass through them
	#		Proof:
	#			An empty node 'A' by definition is a node that has no known path
	#			running through it.  However, as every node must be part of a
	#			path in the solution, we know that A must be on a path.  As
	#			the only parts of a path that do not go to two different points
	#			are the starting head nodes, and an empty node is by definition
	#			not a starting head node, any empty node must have 2 and exactly
	#			2 adjacencies which it moves through.  Thus A has exactly 2
	#			adjacencies which it moves to, and thus if there are only
	#			2 possible adjacencies then it must move through them.
	#
	#	Trivial 4:
	#		If a vertex is surround by 4 adjacencies, 3 of which belong to the
	#		same path, then the fourth one must belong to a different path
	#		Proof:
	#			Assume that this is not true.  Then, it violates rule 3
	#			of the second definition of Flow, that no vertex is surrounded
	#			by four nodes of the same path.
	#
	#		Corrolary:
	#			Let a node N be the node belonging to a new path as deduced in
	#			the previous statement.  This node must have connections going
	#			parallel to the paths: (A,B) and (B,C) where C is the node
	#			diagonal from it and A,C are the other two nodes adjacent to
	#			the same vertex.
	#			Proof:
	#				As N is decidedly not on the same path as (A,B,C) by
	#				Trivial 4, it only has 2 valid adjacencies.  By Trivial 3
	#				it must travel to these adjacencies. These adjacencies are
	#				parallel to the paths (A,B) and (B,C), so QED

def Trivial1(grid):
	#Trivial 1
	#			Runtime: O(n^2)
	for row in grid:
		for tile in row:
			if not l.isHead(tile):
				continue
			adjacents = l.getAdjacentsWithDirections(tile)
			adjacents = [x for x in adjacents if x[0] is not None]#get rid of 'nones'
			adjacents = [x for x in adjacents if not l.connected(x[0],tile)]#get rid of connected tiles
			adjacents = [x for x in adjacents if not l.isWall(x[0])]#get rid of wall tiles
			adjacents = [x for x in adjacents if not (l.wouldIntersect(tile,x[0]) and l.isHead(x[0]))]#get rid of heads that would cause loops
			#get rid of heads that are not the same color as this, unless imaginary
			adjacents = [x for x in adjacents if (not (l.isHead(x[0]) and x[0].number!=tile.number and not tile.imaginary)) or (x[0].imaginary)]
			#adjacents = [x for x in adjacents if not (l.isHead(x[0]) and x[0].number!=tile.number)]
			#if adjacents is only size 1, it only has one possible move:
			if len(adjacents) == 1:
				direc = adjacents[0][1]
				l.addDirection(tile,direc)
				l.addDirection(adjacents[0][0],l.getOpposite(direc))
				#adjacents[0][0].color = tile.color
				adjacents[0][0].number = tile.number
				adjacents[0][0].imaginary = tile.imaginary
				if stepByStep:
					return

def Trivial2(grid):
	#Trivial 2
	#			Runtime: O(n^2)
	for row in grid:
		for tile in row:
			if not l.isHead(tile):
				continue
			adjacents = l.getAdjacentsWithDirections(tile)
			adjacents = [x for x in adjacents if x[0] is not None]#get rid of 'nones'
			#get nodes it is adjacent to
			adjacents = [x for x in adjacents if l.isHead(x[0])]
			adjacents = [x for x in adjacents if x[0].number==tile.number and not (tile.imaginary or x[0].imaginary)]
			#if adjacents is size 1, it is the required move:
			if len(adjacents)==1:
				direc = adjacents[0][1]
				l.addDirection(tile,direc)
				l.addDirection(adjacents[0][0],l.getOpposite(direc))
				adjacents[0][0].number = tile.number
				#Should never connect imaginary heads like this,
				#hence the line below is commented out
				#adjacents[0][0].imaginary = tile.imaginary
				if stepByStep:
					return
def Trivial3(grid):
	#Trivial 3
	#			Runtime: O(n^2)
	for row in grid:
		for tile in row:
			if not l.isEmpty(tile):
				continue
			adjacents = l.getAdjacentsWithDirections(tile)
			adjacents = [x for x in adjacents if x[0] is not None]#get rid of 'nones'
			adjacents = [x for x in adjacents if not l.isWall(x[0])]#get rid of 'walls'
			#if adjacents have size 2, then it is a valid path
			if len(adjacents)==2:
				headsAdjacent = [x for x in adjacents if l.isHead(x[0])]
				realAdjacent = [x for x in headsAdjacent if not x[0].imaginary]
				imaginaryAdjacent = [x for x in headsAdjacent if x[0].imaginary]
				#if all heads adjacent to are imaginary, this line is imaginary
				makeImaginary = len(imaginaryAdjacent) == len(headsAdjacent)
				newNumber = realAdjacent[0][0].number if len(realAdjacent) > 0 else (imaginaryAdjacent[0][0].number if len(imaginaryAdjacent)> 0 else 0)
				if len(headsAdjacent)==0:
					l.numberOfImaginaryLines+=1
					newNumber = l.numberOfImaginaryLines
				#now hook tiles up
				tile.number = newNumber
				tile.imaginary = makeImaginary
				direc = adjacents[0][1]
				l.addDirection(tile,direc)
				l.addDirection(adjacents[0][0],l.getOpposite(direc))
				pathToChange = l.getAllInPath_algorithms(adjacents[0][0])
				for t in pathToChange:
					#turn everything in this path into the new number/imaginarity
					t.number = newNumber
					t.imaginary = makeImaginary
				direc = adjacents[1][1]
				l.addDirection(tile,direc)
				l.addDirection(adjacents[1][0],l.getOpposite(direc))
				pathToChange = l.getAllInPath_algorithms(adjacents[1][0])
				for t in pathToChange:
					#turn everything in this path into the new number/imaginarity
					t.number = newNumber
					t.imaginary = makeImaginary
				if stepByStep:
					return

def Trivial4(grid):
	#Trivial 4
	#			Runtime: O(n^2)
	for row in grid:
		for tile in row:
			adjacents = l.getAdjacentsWithDirections(tile)
			adjacents = [x for x in adjacents if x[0] is not None]#remove none
			adjacents = [x for x in adjacents if x[1]==c.D.s or x[1]==c.D.e]#get south and east
			if len(adjacents)!=2:
				continue#does not have south and east connection
			vertexAdjacents = [x for x in adjacents]
			vertexAdjacents.append((tile,c.D.u))
			southern = [x for x in vertexAdjacents if x[1]==c.D.s][0][0]
			adjacentsOfSouthern = l.getAdjacentsWithDirections(southern)
			adjacentsOfSouthern = [x for x in adjacentsOfSouthern if x[1]==c.D.e]
			vertexAdjacents.append(adjacentsOfSouthern[0])
			numbers = [(x[0].number,x[0].imaginary) for x in vertexAdjacents]
			sameNumbers = [ [x for x in numbers if x[0]==numbers[0][0] and x[1]==numbers[0][1]] ]
			for a in range(1,len(numbers)):
				sameNumbers.append([x for x in numbers if x[0]==numbers[a][0] and x[1]==numbers[a][1]])
			duplicatesRemoved = []
			for a in sameNumbers:
				if not a in duplicatesRemoved:
					duplicatesRemoved.append(a)
			sameNumbers = duplicatesRemoved
			sameNumbers = [x for x in sameNumbers if len(x)==3]
			if len(sameNumbers)==1:
				#3 nodes on same path found
				example = [x for x in vertexAdjacents if x[0].number == sameNumbers[0][0][0]][0]
				uglyDuckling = [x for x in vertexAdjacents if x[0].number!=example[0] or x[0].imaginary!=example[1]][0][0]
				#(don't worry, the duckling is beautiful on the inside)
				#uglyDuckling contains the odd one out.  It should become a single
				#imaginary head with a new number.
				if (l.isEmpty(uglyDuckling)) and not l.isEmpty(example[0]):
					#cases where this doesn't work is if uglyDuckling is already full
					#and where instead of having 3 same-path nodes the vertex merely had
					#3 empty nodes.  I actually think having both requirements is
					#redundant, but just to be safe I'm putting both
					uglyDuckling.imaginary = True
					l.numberOfImaginaryLines+=1
					uglyDuckling.number = l.numberOfImaginaryLines

					#Now, let's do the corollary.
					ducklingAdjacents = l.getAdjacentsWithDirections(uglyDuckling)
					ducklingNotties = [x[0] for x in vertexAdjacents]
					ducklingAdjacents = [x for x in ducklingAdjacents if (x[0] not in ducklingNotties)]

					#resolve de-imaginification
					relevants = [uglyDuckling,ducklingAdjacents[0][0],ducklingAdjacents[1][0]]
					emptyRelevants = [x for x in relevants if l.isEmpty(x)]
					imaginaryRelevants = [x for x in relevants if x.imaginary]
					realRelevants = [x for x in relevants if not x.imaginary and x not in emptyRelevants]

					makeImaginary = False
					newNumber = 0
					if len(realRelevants)==0:
						makeImaginary = True
						if len(emptyRelevants)==3:
							l.numberOfImaginaryLines+=1
							newNumber = l.numberOfImaginaryLines
						else:
							newNumber = imaginaryRelevants[0].number
					else:
						makeImaginary = False
						newNumber = realRelevants[0].number

					#get the mentioned nodes:
					direc = ducklingAdjacents[0][1]
					l.addDirection(uglyDuckling,direc)
					l.addDirection(ducklingAdjacents[0][0],l.getOpposite(direc))
					direc = ducklingAdjacents[1][1]
					l.addDirection(uglyDuckling,direc)
					l.addDirection(ducklingAdjacents[1][0],l.getOpposite(direc))
					uglyDuckling.imaginary = makeImaginary
					uglyDuckling.number = newNumber
					ducklingAdjacents[0][0].imaginary = makeImaginary
					ducklingAdjacents[1][0].imaginary = makeImaginary
					ducklingAdjacents[0][0].number = newNumber
					ducklingAdjacents[1][0].number = newNumber
					if stepByStep:
						return
