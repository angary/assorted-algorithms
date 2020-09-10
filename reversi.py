# Contains the code for implementation of reversi and minimax AI
# REPLACED "B" WITH "." FOR VISIBILTY
# TODO: Add err check for input, alpha beta pruning, heuristic

import math
import copy
import time

# Currently the weights is predefined, hopefully can make an algo to determine
SIZE = 4
MAX_TURN = (SIZE ** 2) - 3
colour = ["W", "."]
dy = [1, 1, 0, -1, -1, -1, 0, 1]
dx = [0, 1, 1, 1, 0, -1, -1, -1]


# Object to contain game data and methods
################################################################################
class Game(object):

	def __init__(self):
		self.b = [["_" for j in range(SIZE)] for i in range(SIZE)]
		self.flip = [[[] for i in range(SIZE)] for j in range(SIZE)]
		self.turn = 0
		mid_s = (SIZE // 2) - 1
		mid_b = SIZE // 2
		self.b[mid_s][mid_s] = colour[0]
		self.b[mid_b][mid_b] = colour[0]
		self.b[mid_s][mid_b] = colour[1]
		self.b[mid_b][mid_s] = colour[1]

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
		if self.find_valid(0) == 0 or self.find_valid(1) == 0:
			return True
		whites = 0
		blacks = 0
		for y in range(SIZE):
			whites += self.b[y].count(colour[0])
			blacks += self.b[y].count(colour[1])
		if whites == 0 or blacks == 0:
			return True
		return False

	# Check if a square is valid
	def valid(self, y, x, player):
		if self.b[y][x] != "_":
			return 0
		curr_colour = colour[player]
		oth_colour = colour[(player + 1) % 2]
		flip_dirs, flipped = self.find_flips(y, x, oth_colour, curr_colour)
		return flipped

	# Find which direction a move flips, and how many it flips
	def find_flips(self, y, x, oth_colour, curr_colour):
		flipped = 0
		flip_dirs = []
		for dir_index in range(len(dx)):
			if not self.in_limits(y + dy[dir_index], x + dx[dir_index]):
				continue
			if self.b[y + dy[dir_index]][x + dx[dir_index]] == oth_colour:
				curr_flipped = 0
				for mul in range(1, SIZE):
					nY = y + mul * dy[dir_index]
					nX = x + mul * dx[dir_index]
					if not self.in_limits(nY, nX):
						break
					if self.b[nY][nX] == curr_colour:
						flip_dirs.append(dir_index)
						flipped += curr_flipped
						break
					curr_flipped += 1
		return flip_dirs, flipped

	# Register the player's chosen location on the board
	def go(self, y, x, player):
		curr_colour = colour[player]
		oth_colour = colour[(player + 1) % 2]
		self.b[y][x] = curr_colour
		flip_dirs = self.find_flips(y, x, oth_colour, curr_colour)[0]
		for dir_index in flip_dirs:
			for mul in range(1, SIZE):
				nY = y + mul * dy[dir_index]
				nX = x + mul * dx[dir_index]
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
	
	# Return the number of white and black squares
	def find_score(self):
		score = {colour[0]: 0, colour[1]: 0}
		for y in range(SIZE):
			for x in range(SIZE):
				if self.b[y][x] == colour[0]:
					score[colour[0]] += 1
				elif self.b[y][x] == colour[1]:
					score[colour[1]] += 1
		return score


# Driver code + code to take human input
################################################################################
def main():
	print("Game started")
	print("Enter positions as <letter><number>, i.e. a1")
	game = Game()
	game.turn = 1
	game.print_board()
	while not game.over():
		player = game.turn % 2
		if player == 1:
			y, x = take_turn(game, player)
			game.go(y, x, player)
		else:
			start_time = time.time()
			best = minimax(game, player, player)
			game.go(best[1], best[2], player)
			print("Time taken:", time.time() - start_time)
		game.print_board()
		print(game.find_score())
		print("Turn is", game.turn)
	print("Game over")
	game.print_board()
	print(game.find_score())


# Take the input from human player
def take_turn(game, player):
	while True:
		print("Currently", colour[player])
		loc = input("Choose position: ")
		x, y = int(ord(loc[0].lower()) - int(ord('a'))), int(loc[1]) - 1
		if game.in_limits(y, x) and game.valid(y, x, player):
			break
		if not game.in_limits(y, x):
			print("Not in limits")
		else:
			print("Not a valid move according to game.valid()")
		print("Invalid location", loc)
	return y, x


# Ai code
################################################################################
def minimax(game, player, prioritise):
	if game.over():
		return (game.find_score()[colour[prioritise]], 0, 0)
	best_eval = -math.inf if player == prioritise else math.inf
	valid_moves = game.find_valid(player)
	best_x = 0
	best_y = 0
	for y, x in valid_moves:
		new_game = copy.deepcopy(game)
		new_game.go(y, x, player)
		new_eval = minimax(new_game, (player + 1) % 2, prioritise)
		if ((player == prioritise and best_eval < new_eval[0])
			or (player != prioritise and best_eval > new_eval[0])):
			best_eval = new_eval[0]
			best_y = y
			best_x = x
	return best_eval, best_y, best_x


if __name__ == "__main__":
	main()
