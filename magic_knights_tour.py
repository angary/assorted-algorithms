# Program to find magic square knights tour
# Doesn't consider diagonals, because I'm not sure if they exist for 8 x 8
# In fact it doesn't even work (idk how long it'll take to find a solution)
# Uses warnsdorff's algo, but augmented to suit magic square conditions
# It also alternate/ backtrack bewteen quartes using a stack
# Maybe those two combined together doesn't result in a solution

dx = [2, 1, -1, -2, -2, -1, 1, 2]
dy = [1, 2, 2, 1, -1, -2, -2, -1]


# Driver code
def main():
	source = input("Starting position: ")
	src = [int(ord(source[0].lower()) - int(ord('a'))), int(source[1]) - 1]
	y = src[0]
	x = src[1]
	b = [[0 for j in range(8)] for i in range(8)]
	b[y][x] = 1
	quarte = quarteLoc(y, x)
	printBoard(b)
	solve(b, src, 1, [quarte], False)
	printBoard(b)


# DFS solve
def solve(b, p, turn, qStack, backTrack):

	# Base case
	if turn == 64:
		return True

	# Find potential moves
	qPrior = findQuarte(backTrack, qStack.copy())
	h = heuristic(b, p, turn + 1, qPrior)
	
	# if turn > 44 and h != None:
	# 	print("BackTrack: \t", backTrack)
	# 	print("qStack: \t", qStack)
	# 	print("qPriority: \t", qPrior)
	# 	print("Turn: \t\t", turn)
	# 	printBoard(b)

	# Check moves w/ DFS backTrack
	for i in range(len(h)):
		y = p[0] + dy[h[i]]
		x = p[1] + dx[h[i]]
		b[y][x] = turn + 1
		tmpStack = qStack.copy()
		newBackTrack = fixStack(quarteLoc(y, x), tmpStack, backTrack)
		if solve(b, [y, x], turn + 1, tmpStack, newBackTrack):
			return True
		b[y][x] = 0
	return False


# Check that the sum of row and col of len 4 is equal to 130
def magic(b, y, x, turn):
	halfRow = b[y][4 * (x > 3):4 * (1 + (x > 3))]
	if min(halfRow) > 0 and sum(halfRow) != 130:
		return False
	halfCol = [b[i][x] for i in range(4 * (y > 3), 4 * (1 + (y > 3)))]
	if min(halfCol) > 0 and sum(halfCol) != 130:
		return False
	return True


# Returns an array of movement array indexes
# Method of sort: Highest degree of magic square potential connections
def heuristic(b, p, turn, qPrior):
	d = []
	loRow = p[0] - (p[0] % 4)
	loCol = p[1] - (p[1] % 4)
	for i in range(8):
		y = p[0] + dy[i]
		x = p[1] + dx[i]
		if valid(b, y, x) and quarteLoc(y, x) in qPrior:
			b[y][x] = turn
			if magic(b, y, x, turn):
				deg = 0
				for j in range(8):
					newY = y + dy[j]
					newX = x + dy[x]
					if valid(b, newY, newX):
						b[newY][newX] = turn + 1
						if magic(b, y + dy[j], x, turn + 1):
							deg += 1
						b[newY][newX] = 0
				d.append([deg, i])
			b[y][x] = 0
	d.sort(key = lambda i: i[0])
	return [d[i][1] for i in range(len(d))]


# Find which quarte to prioritise
def findQuarte(backTrack, qStack):
	
	# If we are back tracking, just prioritise previous quarte
	if backTrack:
		return [qStack[-1]]

	# Calculate potential quartes
	noDups = list(set(qStack))
	numUnique = len(noDups)
	if numUnique == 0:
		return [0, 1, 2, 3]
	currFreq = qStack.count(noDups[numUnique - 1])
	if numUnique == 1:
		if qStack.count(noDups[0]) == 8:
			return [i for i in range(4) if i is not noDups[0]]
		else:
			return [0, 1, 2, 3]
	elif numUnique == 2:
		if qStack.count(noDups[0]) > currFreq:
			return [noDups[1]]
		elif currFreq < 8:
			return [i for i in range(4) if i is not noDups[0]]
		else:
			return [i for i in range(4) if i not in noDups]
	elif numUnique == 3:
		if qStack.count(noDups[1]) > currFreq:
			return [noDups[2]]
		else:
			return [i for i in range(4) if i not in noDups]
	else:
		return [qStack[-1]]


# Fix the quartile back track stack, return if we back track or not
def fixStack(newQuarte, qStack, backTrack):

	# If we are backtracking
	if backTrack: 
		del qStack[-1]
		return len(qStack) != 0
	
	# Else we want to push to stack
	qStack.append(newQuarte)

	# If there are already four quartiles in stack
	if len(set(qStack)) == 4:
		tailFreq = qStack.count(qStack[-1])
		maxFreq = qStack.count(list(set(qStack))[1])

		# If frequency of final stack == largest frequency, start back tracking
		if tailFreq >= maxFreq:
			return True

	return backTrack


# Print out board idk what else to say
def printBoard(b):
	for i in range(8):
		for j in range(8):
			print("%3d" % b[i][j], end="")
		print()
	print()


# Check if square is within the limits of the chessboard
def valid(b, y, x):
	return 0 <= x and x < 8 and 0 <= y and y < 8 and b[y][x] == 0


# Check which quarte the square is in
def quarteLoc(y, x):
	return 2 * (y >= 4) + (x >= 4) 


if __name__ == "__main__":
	main()