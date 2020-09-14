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
	[ 64,  2, 56, 32, 32, 56,  2, 64],
	[  2,  0,  8,  8,  8,  8,  0,  2],
	[ 56,  8, 56, 16, 16, 56,  8, 56],
	[ 32,  8, 16, 16, 16, 16,  8, 32],
	[ 32,  8, 16, 16, 16, 16,  8, 32],
	[ 56,  8, 56, 16, 16, 56,  8, 56],
	[  2,  0,  8,  8,  8,  8,  0, 32],
	[ 64,  2, 56, 32, 32, 56,  2, 64]
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
			start_time = time.time()
			best = negamax(g, player, player, -math.inf, math.inf, 5)
			g.go(best[1], best[2], player)
			# print("checked: ", checked)
			# print("Time taken: {0:.2}".format(time.time() - start_time))
			print("Prediction for best score:", best[0])

		# The "."
		else:
			start_time = time.time()
			best = negamax(g, player, player, -math.inf, math.inf, 1)
			g.go(best[1], best[2], player)
			# print("checked: ", checked)
			# print("Time taken: {0:.2}".format(time.time() - start_time))
			print("Prediction for best score:", best[0])

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


# Dynamic calculation of the weight for each square of current turn
# def calc_weights(g, player):
# 	# CHeck how many values the square can flip
# 	global weights 
# 	return weights


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
		turn_weight = (math.log(g.max_turn - g.turn) / math.log(g.max_turn))
		rating += weights[y][x] * turn_weight
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

	# Number of squares
	score = g.find_score()
	my_score = score[g.colour[player]]
	oth_score = score[g.colour[oth_player]]
	score_weight = g.turn / g.max_turn

	rating += ((my_score - oth_score) / (g.max_turn + 4)) * score_weight
	rating += (my_mobility - oth_mobility) / (my_mobility + oth_mobility + 1)

	return rating


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