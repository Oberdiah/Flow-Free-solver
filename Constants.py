# Size of overall grid (In boxes)
GRIDSIZE = 20
# Size of boxes (In pixels) (Must be even)
BOXSIZE = 1000//GRIDSIZE
# Grid thickness (Must be even)
GRIDTHICKNESS = 2
# The minimum snake length
MINIMUMSNAKELENGTH = GRIDSIZE*3
# Chance for a snake to end every new piece after MINSNAKELENGTH:
SNAKEENDCHANCE = 0.2
# Straightness of lines
STRAIGHTNESS = GRIDSIZE

userGrid = []
solutionGrid = []
computerGrid = []

# Essentially a directions Enum
class D():
	n = (0,1)
	s = (0,-1)
	e = (1,0)
	w = (-1,0)
	u = (0,0)

allDirections = [D.n, D.s, D.e, D.w]

all3x3Directions = [(-1,1),  (0,1),  (1,1),
					(-1,0),          (1,0),
					(-1,-1), (0,-1), (1,-1)]