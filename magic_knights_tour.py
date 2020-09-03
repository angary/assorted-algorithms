# Program to find magic square knights tour
# Utilises backtracking with Warnsdorff algorithm 
# Generates magic square made of regular quartes with quad back tracking
# Enter input like 'a1' or 'h4'

dx = [2, 1, -1, -2, -2, -1, 1, 2]
dy = [1, 2, 2, 1, -1, -2, -2, -1]
max_stack = 16


# Driver code
def main():
	source = input("Starting position: ")
	y, x = int(ord(source[0].lower()) - int(ord('a'))), int(source[1]) - 1
	b = [[0 for j in range(8)] for i in range(8)]
	b[y][x] = 1
	print_board(b)
	if (((y == 2 or y == 5) and (x == 3 or x == 4))
		or ((y == 3 or y == 4) and (x == 2 or x == 5))):
		global max_stack
		max_stack = 32
	if solve(b, [y, x], 1, [quad_hash(y, x)], False):
		print_board(b)
	else:
		print("Could not find solution")


# Backtracking solve
def solve(b, pos, turn, quad_stack, backtrack):
	if turn == 64:
		return True
	if backtrack and len(quad_stack) == 0: 
		backtrack = False
	if not backtrack and len(quad_stack) == max_stack: 
		backtrack = True
	quads = find_quad(quad_stack, backtrack)
	directions = heuristic(b, pos, turn + 1, quads)
	for i in range(len(directions)):
		y = pos[0] + dy[directions[i]]
		x = pos[1] + dx[directions[i]]
		b[y][x] = turn + 1
		newStack = quad_stack.copy()
		if not backtrack: 
			newStack.append(quad_hash(y, x))
		if solve(b, [y, x], turn + 1, newStack, backtrack):
			return True
		b[y][x] = 0
	return False


# Return priority queue of directions to go to
def heuristic(b, pos, turn, quads):
	directions = []
	for i in range(8):
		y = pos[0] + dy[i]
		x = pos[1] + dx[i]
		if is_magic(b, y, x, turn) and quad_hash(y, x) in quads:
			degree = 0
			for j in range(8):
				if is_magic(b, y + dy[j], x + dx[j], turn + 1):
					degree += 1
			directions.append([degree, i])
	directions.sort(key = lambda i:i[0])
	return [directions[i][1] for i in range(len(directions))]


# Find which quad to prioritise
def find_quad(quad_stack, backtrack):
	if backtrack:
		return [quad_stack.pop()]
	if len(list(set(quad_stack))) % 16 == 0:
		return [0, 1, 2, 3]
	if quad_stack.count(quad_stack[-1]) % 4 != 0:
		return [quad_stack[-1]]
	recent = quad_stack[16 * (len(quad_stack) // 16):]
	return [i for i in range(4) if i not in recent]


# Print out the chess board
def print_board(b):
    for i in range(8):
        for j in range(8):
            print("%2d " % b[i][j], end = "")
        print()
    print()


# Check which quad the square is in (currently only works for 8 x 8)
def quad_hash(y, x):
	return 2 * (y > 3) + (x > 3)


# Check if the new move satisfies magic condition
def is_magic(b, y, x, turn):
	if x < 0 or x > 7 or y < 0 or y > 7 or b[y][x] != 0:
		return False
	tmp_board = [row[:] for row in b]
	tmp_board[y][x] = turn
	half_row = tmp_board[y][4 * (x > 3) : 4 * (1 + (x > 3))]
	for val in half_row:
		if val > 0 and val != turn and (val - 1) // 4 == (turn - 1) // 4:
			return False
	half_col = [tmp_board[i][x] for i in range(4 * (y > 3), 4 * (1 + (y > 3)))]
	for val in half_col:
		if val > 0 and val != turn and (val - 1) // 4 == (turn - 1) // 4:
			return False
	row = tmp_board[y]
	if min(row) > 0 and sum(row) != 260:
		return False
	col = [tmp_board[i][x] for i in range(8)]
	if min(col) > 0 and sum(col) != 260:
		return False
	return True


if __name__ == "__main__":
	main()
