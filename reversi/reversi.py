# Contains the code for implementation of reversi and minimax AI
# REPLACED "B" WITH "." FOR VISIBILTY
# TODO:
# - Transposition table (not suitable due to alpha beta pruning, maybe)
# - Iterative deepening
# - Principal variation search

from game import Game
import math
import copy
import time

# Global variables because I'm lazy
checked = 0
transposition_table = {}
weights = [
	[ 512,-256, 256, -16, -16, 256,-256, 512],
	[-256,-256, -32, -32, -32, -32,-256,-256],
	[ 256, -32, 256,  16,  16, 256, -32, 256],
	[ -16, -32,  16,  16,  16,  16, -32, -16],
	[ -16, -32,  16,  16,  16,  16, -32, -16],
	[ 256, -32, 256,  16,  16, 256, -32, 256],
	[-256,-256, -32, -32, -32, -32,-256,-256],
	[ 512,-256, 256, -16, -16, 256,-256, 512]
]

# Driver code + code to take human input
################################################################################
def main():
	g = Game()
	print("Game started")
	print("Enter positions as <letter><number>, i.e. a1")
	g.print_board()
	start_time = time.time()
	
	# Depth for minimax search
	depth = 5

	while not g.over():

		# Take input
		curr = checked
		if g.p == 0: 
			human_turn(g, g.p)
		else:
			computer_turn(g, depth)
		
		# Print out values
		print("Player is", g.p)
		g.print_board()
		print(g.find_score())
		print("Turn is", g.turn, "\ttotal:", checked, "\tprev:", checked - curr)

		if g.turn > 50:
			depth += 1

	# Game over
	print("Checked:", checked)
	print("Game over")
	print("Time taken: {}" .format(time.time() - start_time))
	g.print_board()
	print(g.find_score())


# Take the input from human player
def human_turn(g, player):
	while True:
		print("Currently", g.colour[player])
		# try:
		loc = input("Choose position: ").strip()
		if loc == "u" or loc == "U":
			g.undo()
			return
		else:
			x, y = int(ord(loc[0].lower()) - int(ord('a'))), int(loc[1]) - 1
			if g.in_lim(y, x) and g.valid(y, x, player):
				break
			print("Invalid location", loc)
		# except:
			# print("Invalid input")
	g.go(y, x)


# Take the computer's turn
def computer_turn(g, depth):
	best = minimax(g, g.p, -math.inf, math.inf, depth)
	g.go(best[1], best[2])


# AI utils
################################################################################
# Generates a zobrist key for the board
def zobrist_key(g):
	mul = 1
	key = 0
	for y in range(8):
		for x in range(8):
			piece = g.b[y][x]
			if piece != g.blank:
				key += piece * mul
			else:
				key += 2 * mul
			mul *= 3
	return key


# Actual AI algorithm (Computer Sciency stuff)
################################################################################
# Main code
def minimax(g, priority, alpha, beta, depth):

	if g.over() or depth == 0:
		key = zobrist_key(g)
		if key in transposition_table:
			score = transposition_table[key]
		else:
			score = heuristic_score(g, priority)
			transposition_table[key] = score
		return (score, -1, -1)

	global checked
	checked += 1

	valid_moves = heuristic_sort(g, g.find_valid(g.p))
	best_y, best_x = valid_moves[0]
	best_eval = -math.inf if g.p == priority else math.inf

	for y, x in valid_moves:
		new = copy.deepcopy(g)
		new.go(y, x)
		new_eval = minimax(new, priority, alpha, beta, depth - 1)
		new_eval = new_eval[0]
		if g.p == priority:
			if new_eval > best_eval:
				best_eval = new_eval
				best_y = y
				best_x = x
			alpha = max(alpha, best_eval)
		else:
			if new_eval < best_eval:
				best_eval = new_eval
				best_y = y
				best_x = x
			beta = min(beta, best_eval)
		if beta <= alpha:
			break
	return best_eval, best_y, best_x


# Sort moves according to which one seems better
def heuristic_sort(g, valid_moves):
	sorted_moves = []
	for move in valid_moves:
		y, x = move
		# Make the mov and check the score of the new game
		# sorted_moves.append({"move": move, "weight": weights[y][x]})
		new = copy.deepcopy(g)
		new.go(y, x)
		rating = heuristic_score(new, g.p)
		sorted_moves.append({"move": move, "rating": rating})
	sorted_moves.sort(key = lambda x:x["rating"], reverse = True)
	return [move["move"] for move in sorted_moves]


# AI Heuristic stuff
################################################################################

# Score the game using the heuristic
def heuristic_score(g, p):
	rating = 0
	oth_p = (p + 1) % 2

	# Mobility of current turn
	my_mobility = len(g.find_valid(p))
	oth_mobility = len(g.find_valid(oth_p))
	total_mobility = my_mobility + oth_mobility
	mobility = (my_mobility - oth_mobility) / max(total_mobility, 1)

	# PLayer Corner count
	corners = corner_count(g)
	my_corners = corners[p]
	oth_corners = corners[oth_p]
	total_corners = my_corners + oth_corners
	corner = (my_corners - oth_corners) / max(total_corners, 1)

	# PLayer frontier count
	my_frontier = frontier_count(g, p)
	oth_frontier = frontier_count(g, oth_p)
	frontier = (my_frontier - oth_frontier) / max((my_frontier + oth_frontier), 1)

	# Weight of squares and their stabilty
	weights = stabs = [0, 0]
	for y in range(8):
		for x in range(8):
			if g.b[y][x] != g.blank:
				piece = g.b[y][x]
				weights[piece] += square_stability(g, y, x)
				stabs[piece] += square_weight(g, y, x)
	my_weight = weights[p]
	oth_weight = weights[oth_p]
	stability = (stabs[p] - stabs[oth_p]) / max((stabs[p] + stabs[oth_p]), 1)
	weight = (my_weight - oth_weight) / max((my_weight + oth_weight), 1)


	rating += corner * 6
	rating += (1 - g.turn / 60) * (frontier +  mobility + weight)
	rating += (1 + (3 * g.turn) / 60) * stability

	return rating


# Find the stability of a square
def square_stability(g, y, x):
	stability = 4096
	
	# CAN ALSO REIMPLEMENT USING DIR VEC ARRAY
	row = g.b[y]
	col = [g.b[i][x] for i in range(8)]
	left = right = above = below = 0
	for i in range(8):
		if i < x and row[i] == g.blank:
			left += 1
		elif i > x and row[i] == g.blank:
			right += 1
		if i < y and col[i] == g.blank:
			below += 1
		elif i > y and col[i] == g.blank:
			above += 1
	stability /= 2 ** (min(left, right) + min(above, below))

	# Check top left, and top right diagonals
	tl_above = tl_below = tr_above = tr_below = 0
	tl_y = 7 - x
	tl_x = 0
	tr_y = x
	tr_x = 7
	for i in range(8):
		if g.in_lim(tl_y, tl_x) and g.b[tl_y][tl_x] == g.blank:
			if tl_y > y:
				tl_above += 1
			elif tl_y < y:
				tl_below += 1
		if g.in_lim(tr_y, tr_x) and g.b[tr_y][tr_x] == g.blank:
			if tr_y > y:
				tr_above += 1
			elif tr_y < y:
				tr_below += 1
		tl_y -= 1
		tr_y -= 1
		tl_x += 1
		tr_x -= 1
	stability /= 2 ** (min(tl_above, tl_below) + min(tr_above, tr_below))
	return stability


# Find the weight/ value of a square
def square_weight(g, y, x):
	# IMPLEMENT DYNAMIC SQUARE WEIGHTS
	weight = weights[y][x]
	# Scuffed method for testing
	if (((y == 1 and (x == 0 or x == 1)) or (y == 0 and x == 1) and (g.b[0][0] != g.blank))
		or ((y == 1 and (x == 6 or x == 7)) or (y == 0 and x == 7) and (g.b[0][7] != g.blank))
		or ((y == 6 and (x == 0 or x == 1)) or (y == 7 and x == 1) and (g.b[7][0] != g.blank))
		or ((y == 6 and (x == 6 or x == 7)) or (y == 7 and x == 6) and (g.b[7][7] != g.blank))):
		weight = 48
			
	return weight


# Find how many corner a player owns
def corner_count(g):
	corners = [0, 0]
	if g.b[0][0] != g.blank:
		corners[g.b[0][0]] += 1
	if g.b[7][0] != g.blank:
		corners[g.b[7][0]] += 1
	if g.b[0][7] != g.blank:
		corners[g.b[0][7]] += 1
	if g.b[7][7] != g.blank:
		corners[g.b[7][7]] += 1
	return corners


# Check number of the squares on the player's frontier
def frontier_count(g, player):
	dy = [ 1, 0,-1, 0]
	dx = [ 0, 1, 0,-1]
	count = 0
	for y in range(8):
		for x in range(8):
			if g.b[y][x] == player:
				for i in range(4):
					nY = y + dy[i]
					nX = x + dx[i]
					if g.in_lim(nY, nX) and g.b[nY][nX] != player:
						count += 1
	return count


if __name__ == "__main__":
	main()


# Random notes
# For (size 8, heuristic v1.0, depth = 5, unsorted):
#	checks = 17702
# For (size 8, heuristic v1.0, depth = 5, sorted):
#	checks = 33333
# For (size 8, heuristic v1.0, depth = 6, unsorted):
#	checks = 79042
# For (size 8, heuristic v1.0, depth = 6, sorted):
#	checks = 43172
# For (size 8, heuristic v1.0, depth = 7, unsorted): 
#	checks = 123289
# For (size 8, heuristic v1.0, depth = 7, sorted):
#	checks = 167067 idk why checks is more feelsbadman