# Program to find magic square knights tour
# Utilises backtracking with Warnsdorff algorithm 
# Generates magic square made of regular quartes with quad back tracking
# Enter input like 'a1' or 'h4'

dx = [2, 1, -1, -2, -2, -1, 1, 2]
dy = [1, 2, 2, 1, -1, -2, -2, -1]


# Driver code
def main():
	source = input("Starting position: ")
	y, x = int(ord(source[0].lower()) - int(ord('a'))), int(source[1]) - 1
	b = [[0 for j in range(8)] for i in range(8)]
	b[y][x] = 1
	printBoard(b)
	maxStack = 16
	if (((y == 2 or y == 5) and (x == 3 or x == 4)) or
		((y == 3 or y == 4) and (x == 2 or x == 5))):
		maxStack = 32
	if solve(b, [y, x], 1, [quadHash(y, x)], False, maxStack):
		printBoard(b)
	else:
		print("Could not find solution")


# Backtracking solve
def solve(b, pos, turn, qStack, backtrack, maxStack):
	if turn == 64:
		return True
	if backtrack and len(qStack) == 0: 
		backtrack = False
	if not backtrack and len(qStack) == maxStack: 
		backtrack = True
	quads = findQuad(qStack, backtrack)
	pq = heuristic(b, pos, turn + 1, quads)
	for i in range(len(pq)):
		x = pos[1] + dx[pq[i]]
		y = pos[0] + dy[pq[i]]
		b[y][x] = turn + 1
		newStack = qStack.copy()
		if not backtrack: 
			newStack.append(quadHash(y, x))
		if solve(b, [y, x], turn + 1, newStack, backtrack, maxStack):
			return True
		b[y][x] = 0
	return False


# Return priority queue of directions to go to
def heuristic(b, pos, turn, quads):
	d = []
	for i in range(8):
		x = pos[1] + dx[i]
		y = pos[0] + dy[i]
		if isMagic(b, y, x, turn) and quadHash(y, x) in quads:
			degree = 0
			for j in range(8):
				nY = y + dy[j]
				nX = x + dx[j]
				if isMagic(b, nY, nX, turn + 1):
					degree += 1
			d.append([degree, i])
	d.sort(key = lambda i:i[0])
	return [d[i][1] for i in range(len(d))]


# Find which quad to prioritise
def findQuad(qStack, backtrack):
	if backtrack:
		return [qStack.pop()]
	if len(list(set(qStack))) % 16 == 0:
		return [0, 1, 2, 3]
	if qStack.count(qStack[-1]) % 4 != 0:
		return [qStack[-1]]
	return [i for i in range(4) if i not in qStack[16 * (len(qStack) // 16) : ]]


# Print out the chess board
def printBoard(b):
    for i in range(8):
        for j in range(8):
            print("%2d " % b[i][j], end = "")
        print()
    print()


# Check which quad the square is in (currently only works for 8 x 8)
def quadHash(y, x):
	return 2 * (y > 3) + (x > 3)


# Check if the new move satisfies magic condition
def isMagic(b, y, x, turn):
	if x < 0 or x > 7 or y < 0 or y > 7 or b[y][x] != 0:
		return False
	tmpBoard = [row[:] for row in b]
	tmpBoard[y][x] = turn
	halfRow = tmpBoard[y][4 * (x > 3) : 4 * (1 + (x > 3))]
	for val in halfRow:
		if val > 0 and val != turn and (val - 1) // 4 == (turn - 1) // 4:
			return False
	halfCol = [tmpBoard[i][x] for i in range(4 * (y > 3), 4 * (1 + (y > 3)))]
	for val in halfCol:
		if val > 0 and val != turn and (val - 1) // 4 == (turn - 1) // 4:
			return False
	row = tmpBoard[y]
	col = [tmpBoard[i][x] for i in range(8)]
	if (min(row) > 0 and sum(row) != 260) or (min(col) > 0 and sum(col) != 260):
		return False
	return True


if __name__ == "__main__":
	main()
