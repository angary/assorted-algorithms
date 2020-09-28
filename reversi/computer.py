import math
import copy
from reversi import checked

# Global variables because I'm lazy
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


# Actual AI algorithm (Computer Sciency stuff)
################################################################################
# Main code
def minimax(g, priority, alpha, beta, depth):

	if g.over() or depth == 0:
		return find_score(g, priority)

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
		new = copy.deepcopy(g)
		new.go(y, x)
		rating = heuristic_score(new, g.p)
		sorted_moves.append({"move": move, "rating": rating})
	sorted_moves.sort(key = lambda x:x["rating"], reverse = True)
	return [move["move"] for move in sorted_moves]


# Finds the score of the baord
def find_score(g, priority):
	key = zobrist_key(g)
	if key in transposition_table:
		score = transposition_table[key]
	else:
		score = heuristic_score(g, priority)
		transposition_table[key] = score
	return (score, -1, -1)


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


# AI Heuristic (Mathyish stuff)
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
