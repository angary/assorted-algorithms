# Contains the code for implementation of reversi and minimax AI
# REPLACED "B" WITH "." FOR VISIBILTY
# TODO:
# - Dynamic weight calculation
# - Transposition table (not suitable due to alpha beta pruning, maybe)
# - Iterative deepening
# - Principal variation search

import math
import copy
import time

SIZE = 8
MAX_TURN = (SIZE ** 2) - 3
BLANK = "_"
COLOUR = ["W", "."]
DY = [1, 1, 0, -1, -1, -1, 0, 1]
DX = [0, 1, 1, 1, 0, -1, -1, -1]

weights = [[0 for j in range(SIZE)] for i in range(SIZE)]
checked = 0


# Object to contain game data and methods
################################################################################
class Game(object):

	def __init__(self):
		self.b = [[BLANK for j in range(SIZE)] for i in range(SIZE)]
		self.flip = [[[] for i in range(SIZE)] for j in range(SIZE)]
		self.turn = 0
		mid_s = (SIZE // 2) - 1
		mid_b = SIZE // 2
		self.b[mid_s][mid_s] = COLOUR[0]
		self.b[mid_b][mid_b] = COLOUR[0]
		self.b[mid_s][mid_b] = COLOUR[1]
		self.b[mid_b][mid_s] = COLOUR[1]

	# Print out the board
	def print_board(self):
		print()
		print("   a b c d e f g h")
		print("   _______________")
		for i in range(SIZE):
			print(i + 1, "|", end="")
			for j in range(SIZE):
				print(self.b[i][j], end=" ")
			print()
		print()

	# Check if the game is over
	def over(self):
		if self.turn == MAX_TURN:
			return True
		if len(self.find_valid(0)) == 0 or len(self.find_valid(1)) == 0:
			return True
		whites = 0
		blacks = 0
		for y in range(SIZE):
			whites += self.b[y].count(COLOUR[0])
			blacks += self.b[y].count(COLOUR[1])
		if whites == 0 or blacks == 0:
			return True
		return False

	# Return the number of white and black squares
	def find_score(self):
		score = {COLOUR[0]: 0, COLOUR[1]: 0}
		for y in range(SIZE):
			for x in range(SIZE):
				if self.b[y][x] == COLOUR[0]:
					score[COLOUR[0]] += 1
				elif self.b[y][x] == COLOUR[1]:
					score[COLOUR[1]] += 1
		return score

	# Register the player's chosen location on the board
	def go(self, y, x, player):
		curr_colour = COLOUR[player]
		oth_colour = COLOUR[(player + 1) % 2]
		self.b[y][x] = curr_colour
		flip_dirs = self.find_flips(y, x, oth_colour, curr_colour)[0]
		for dir_index in flip_dirs:
			for mul in range(1, SIZE):
				nY = y + mul * DY[dir_index]
				nX = x + mul * DX[dir_index]
				if not self.in_limits(nY, nX) or self.b[nY][nX] == curr_colour:
					break
				self.b[nY][nX] = curr_colour
		self.turn += 1

	# Check if a location is in the board
	def in_limits(self, y, x):
		return not (y < 0 or y >= SIZE or x < 0 or x >= SIZE)

	# Finds all valid locations for a player
	def find_valid(self, player):
		valid_moves = []
		for y in range(SIZE):
			for x in range(SIZE):
				if self.valid(y, x, player):
					valid_moves.append((y, x))
		return valid_moves

	# Check if a square is valid
	def valid(self, y, x, player):
		if self.b[y][x] != BLANK:
			return 0
		curr_colour = COLOUR[player]
		oth_colour = COLOUR[(player + 1) % 2]
		flip_dirs, flipped = self.find_flips(y, x, oth_colour, curr_colour)
		return flipped

	# Find which direction a move flips, and how many it flips
	def find_flips(self, y, x, oth_colour, curr_colour):
		flipped = 0
		flip_dirs = []
		for dir_index in range(len(DX)):
			if not self.in_limits(y + DY[dir_index], x + DX[dir_index]):
				continue
			if self.b[y + DY[dir_index]][x + DX[dir_index]] == oth_colour:
				curr_flipped = 0
				for mul in range(1, SIZE):
					nY = y + mul * DY[dir_index]
					nX = x + mul * DX[dir_index]
					if not self.in_limits(nY, nX) or self.b[nY][nX] == BLANK:
						break
					if self.b[nY][nX] == curr_colour:
						flip_dirs.append(dir_index)
						flipped += curr_flipped
						break
					curr_flipped += 1
		return flip_dirs, flipped


# Driver code + code to take human input
################################################################################
def main():
	global weights

	# Calculate the weights
	for i in range(SIZE):
		for j in range(SIZE):
			weights[i][j] += max(i, SIZE - 1 - i)
			weights[i][j] += max(j, SIZE - 1 - j)
			if (i == 0 or i == SIZE - 1) and (j == 1 or j == SIZE - 2):
				weights[i][j] = 0
			elif ((j == 0 or j == 1 or j == SIZE - 1 or j == SIZE - 2) 
				and (i == 1 or i == SIZE - 2)):
				weights[i][j] = 0

	print("Game started")
	print("Enter positions as <letter><number>, i.e. a1")
	game = Game()
	game.turn = 1
	game.print_board()
	start_time = time.time()
	global checked

	# Game loop
	while not game.over():
		player = game.turn % 2
		# print("Valid moves is", game.find_valid(player))
		# checked = 0

		# Take human input (The white)
		if player == 0: 
			# y, x = take_turn(game, player)
			# game.go(y, x, player)
			# checked = 0
			# start_time = time.time()
			depth = MAX_TURN // 2
			best = negamax(game, player, player, -math.inf, math.inf, 6)
			game.go(best[1], best[2], player)
			print("checked: ", checked)
			# print("Prediction for best score:", best[0])
			# print("Time taken: {0:.2}".format(time.time() - start_time))

		# Take AI input (The dot)
		else:
			# start_time = time.time()
			depth = 5
			best = negamax(game, player, player, -math.inf, math.inf, 4)
			game.go(best[1], best[2], player)
			print("checked: ", checked)
			# print("Prediction for best score:", best[0])
			# print("Time taken: {0:.2}".format(time.time() - start_time))

		# game.print_board()
		# print(game.find_score())
		# print("Turn is", game.turn)
	
	print("Game over")
	print("Time taken: {}" .format(time.time() - start_time))
	game.print_board()
	print(game.find_score())


# Take the input from human player
def take_turn(game, player):
	while True:
		print("Currently", COLOUR[player])
		try:
			loc = input("Choose position: ")
			x, y = int(ord(loc[0].lower()) - int(ord('a'))), int(loc[1]) - 1
			if game.in_limits(y, x) and game.valid(y, x, player):
				break
			print("Invalid location", loc)
		except:
			print("Invalid input")
	return y, x


# Ai code
################################################################################
def negamax(game, player, me, alpha, beta, depth):
	if game.over() or depth == 0:
		if depth != 0 and game.turn > MAX_TURN * (3 / 4):
			oth = (me + 1) % 2
			score = (heuristic_score(game, me) - heuristic_score(game, oth))
		else:
			score = game.find_score()[COLOUR[player]] - (game.turn + 4) // 2
		return (score, 0, 0)

	global checked
	checked += 1

	best_eval = -math.inf
	valid_moves = game.find_valid(player)
	valid_moves = heuristic_sort(game, player, valid_moves)
	best_y, best_x = valid_moves[0]

	for y, x in valid_moves:
		new = copy.deepcopy(game)
		new.go(y, x, player)
		oth_player = (player + 1) % 2
		new_eval = negamax(new, oth_player, me, -beta, -alpha, depth - 1)
		if best_eval < -new_eval[0]:
			best_eval = -new_eval[0]
			best_y = y
			best_x = x
		alpha = max(alpha, best_eval)
		if beta <= alpha:
			break
	return best_eval, best_y, best_x


# Sort moves according to which one seems better
def heuristic_sort(game, player, valid_moves):
	sorted_moves = []
	for move in valid_moves:
		y, x = move
		sorted_moves.append({"move": move, "weight": weights[y][x]})
	sorted_moves.sort(key = lambda x:x["weight"], reverse = True)
	return [move["move"] for move in sorted_moves]


# Score the game using the heuristic
def heuristic_score(game, player):
	score = 0
	me = COLOUR[player]
	for y in range(SIZE):
		for x in range(SIZE):
			if game.b[y][x] == me:
				score += weights[y][x]
	return score


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