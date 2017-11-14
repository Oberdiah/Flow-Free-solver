#performs algorithms
import Constants as c

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

def trysolve():
	#print(c.grid)
	c.grid = trytrivials(c.grid)

def trytrivials(grid):
	#This function attempts trivial solves on the grid.
	#A trivial solve is the following:
	#If a head node has 1 adjacency and only 1, it must
	#move there.  This is provable:
	#Let H be a head node with one adjacency A.  There must be a path P from H
	#to its corresponding H'.  Let P pass through an adjacency other than A.
	#Then, there is a contradiction, as there is no such adjacency other than A.
	#Thus, A is on path P.
	
