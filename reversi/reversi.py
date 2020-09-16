# Contains the code for implementation of reversi and minimax AI
# REPLACED "B" WITH "." FOR VISIBILTY
# TODO:
# - Dynamic weight calculation
# - Transposition table (not suitable due to alpha beta pruning, maybe)
# - Iterative deepening
# - Principal variation search

from game import Game
import math
import copy
import time

checked = 0
weights = [
	[ 64,-32, 56, 32, 32, 56,-32, 64],
	[-32,-64,  8,  8,  8,  8,-64,-32],
	[ 56,  8, 56, 16, 16, 56,  8, 56],
	[ 32,  8, 16, 16, 16, 16,  8, 32],
	[ 32,  8, 16, 16, 16, 16,  8, 32],
	[ 56,  8, 56, 16, 16, 56,  8, 56],
	[-32,-64,  8,  8,  8,  8,-64,-32],
	[ 64,-32, 56, 32, 32, 56,-32, 64]
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
		player = g.turn % 2
		# print("Valid moves is", g.find_valid(player))
		# checked = 0

		# The "W"
		if player == 0: 
			# y, x = take_turn(g, player)
			# g.go(y, x, player)
			best = negamax(g, player, player, -math.inf, math.inf, 4)
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

	# weights = calc_weights(g, player)

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
		oth_player = (player + 1) % 2
		new_eval = negamax(new, oth_player, priority, -beta, -alpha, depth - 1)
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
	mobility = (my_mobility - oth_mobility) / (my_mobility + oth_mobility + 1)

	# Weight of squares and their stabilty
	my_weight = oth_weight = my_stab = oth_stab = 0
	for y in range(g.size):
		for x in range(g.size):
			if g.b[y][x] == player:
				my_stab += square_stability(g, player, y, x)
				my_weight += square_weight(g, player, y, x)
			elif g.b[y][x] == oth_player:
				oth_stab += square_stability(g, oth_player, y, x)
				oth_weight += square_weight(g, oth_player, y, x)

	stability = (my_stab - oth_stab) / max((my_stab + oth_stab), 1)
	weight = (my_weight - oth_weight) / max((my_weight + oth_weight), 1)
	# Stability of squares
	rating += mobility
	rating += weight
	rating += stability

	return rating


# Find the stability of a square
def square_stability(g, player, y, x):
	stability = 4096
	row = g.b[y]
	col = [g.b[i][x] for i in range(8)]
	left = right = above = below = 0
	for i in range(g.size):
		if i < x and row[i] == g.blank:
			left += 1
		elif i > x and row[i] == g.blank:
			right += 1
		if i < y and col[i] == g.blank:
			below += 1
		elif i > y and col[i] == g.blank:
			above += 1
	stability /= 2 ** (min(left, right) + min(above, below))

	return stability


# Find the weight/ value of a square
def square_weight(g, player, y, x):
	weight = weights[y][x]
	return weight

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