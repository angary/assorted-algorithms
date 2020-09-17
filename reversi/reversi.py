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

checked = 0
weights = [
	[512,-64,256,-16,-16,256,-64,512],
	[-64,-56,-32,-32,-32,-32,-56,-64],
	[256,-32,256, 16, 16,256,-32,256],
	[-16,-32, 16, 16, 16, 16,-32,-16],
	[-16,-32, 16, 16, 16, 16,-32,-16],
	[256,-32,256, 16, 16,256,-32,256],
	[-64,-56,-32,-32,-32,-32,-56,-64],
	[512,-64,256,-16,-16,256,-64,512]
]

# Driver code + code to take human input
################################################################################
def main():
	g = Game()

	print("Game started")
	print("Enter positions as <letter><number>, i.e. a1")
	g.print_board()
	start_time = time.time()
	global checked

	# g loop
	while not g.over():
		player = g.player
		# print("Valid moves is", g.find_valid(player))
		# checked = 0

		# The "W"
		if player == 0: 
			# y, x = take_turn(g, player)
			# g.go(y, x, player)
			best = negamax(g, player, player, -math.inf, math.inf, 1)
			g.go(best[1], best[2], player)
			# print("checked: ", checked)

		# The "."
		else:
			best = negamax(g, player, player, -math.inf, math.inf, 1)
			g.go(best[1], best[2], player)
			# print("checked: ", checked)

		g.print_board()
		print(g.find_score())
		print("Turn is", g.turn)
	
	print("Game over")
	print("Time taken: {}" .format(time.time() - start_time))
	g.print_board()
	print(g.find_score())


# Take the input from human player
def take_turn(g, player):
	while True:
		print("Currently", g.colour[player])
		try:
			loc = input("Choose position: ")
			x, y = int(ord(loc[0].lower()) - int(ord('a'))), int(loc[1]) - 1
			if g.in_lim(y, x) and g.valid(y, x, player):
				break
			print("Invalid location", loc)
		except:
			print("Invalid input")
	return y, x


# Ai code
################################################################################

# Main code
def negamax(g, player, priority, alpha, beta, depth):

	if g.over() or depth == 0:
		return (heuristic_score(g, priority), -1, -1)

	global checked
	checked += 1

	best_eval = -math.inf
	valid_moves = g.find_valid(player)
	valid_moves = heuristic_sort(g, player, valid_moves)
	best_y, best_x = valid_moves[0]

	for y, x in valid_moves:
		new = copy.deepcopy(g)
		new.go(y, x, player)
		new_eval = negamax(new, g.player, priority, -beta, -alpha, depth - 1)
		if best_eval < -new_eval[0]:
			best_eval = -new_eval[0]
			best_y = y
			best_x = x
		alpha = max(alpha, best_eval)
		if beta <= alpha:
			break
	return best_eval, best_y, best_x


# Sort moves according to which one seems better
def heuristic_sort(g, player, valid_moves):
	sorted_moves = []
	for move in valid_moves:
		y, x = move
		# Make the mov and check the score of the new game
		# sorted_moves.append({"move": move, "weight": weights[y][x]})
		new = copy.deepcopy(g)
		new.go(y, x, player)
		rating = heuristic_score(new, player)
		sorted_moves.append({"move": move, "rating": rating})
	sorted_moves.sort(key = lambda x:x["rating"], reverse = True)
	return [move["move"] for move in sorted_moves]


# Score the game using the heuristic
def heuristic_score(g, player):
	rating = 0
	oth_player = (player + 1) % 2

	# Mobility of current turn
	my_mobility = len(g.find_valid(player))
	oth_mobility = len(g.find_valid(oth_player))
	mobility = (my_mobility - oth_mobility) / max((my_mobility + oth_mobility), 1)

	# PLayer Corner count
	my_corners = corner_count(g, player)
	oth_corners = corner_count(g, oth_player)
	corner = (my_corners - oth_corners) / max((my_corners + oth_corners), 1)

	# PLayer frontier count
	my_frontier = frontier_count(g, player)
	oth_frontier = frontier_count(g, oth_player)
	frontier = (my_frontier - oth_frontier) / max((my_frontier + oth_frontier), 1)

	# Weight of squares and their stabilty
	my_weight = oth_weight = my_stab = oth_stab = 0
	for y in range(8):
		for x in range(8):
			if g.b[y][x] == player:
				my_stab += square_stability(g, player, y, x)
				my_weight += square_weight(g, player, y, x)
			elif g.b[y][x] == oth_player:
				oth_stab += square_stability(g, oth_player, y, x)
				oth_weight += square_weight(g, oth_player, y, x)
	stability = (my_stab - oth_stab) / max((my_stab + oth_stab), 1)
	weight = (my_weight - oth_weight) / max((my_weight + oth_weight), 1)

	# Also add checks for corners and frontier length

	rating += corner * 256
	rating += frontier * (1 - (g.turn / 60))
	rating += mobility * (1 - (g.turn / 60))
	rating += weight
	rating += stability

	return rating


# Find the stability of a square
def square_stability(g, player, y, x):
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

	tl_above = tl_below = tr_above = tr_below = 0
	tl_y = 8 - x - 1
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
	stability /= 2 **(min(tl_above, tl_below) + min(tr_above, tr_below))
	return stability


# Find the weight/ value of a square
def square_weight(g, player, y, x):
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
def corner_count(g, player):
	corners = 0
	if g.b[0][0] == player:
		corners += 1
	if g.b[7][0] == player:
		corners += 1
	if g.b[0][7] == player:
		corners += 1
	if g.b[7][7] == player:
		corners += 1
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