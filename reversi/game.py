


# Object to contain game data and methods
################################################################################
class Game(object):

	def __init__(self, size = 8):
		self.size = size
		self.turn = 0
		self.max_turn = (size ** 2) - 4
		self.blank = "_"
		self.colour = ["W", ".", "_"]
		self.dy = [1, 1, 0, -1, -1, -1, 0, 1]
		self.dx = [0, 1, 1, 1, 0, -1, -1, -1]
		self.b = [[self.blank for j in range(size)] for i in range(size)]
		mid_s = (size // 2) - 1
		mid_b = size // 2
		self.b[mid_s][mid_s] = 1
		self.b[mid_b][mid_b] = 1
		self.b[mid_s][mid_b] = 0
		self.b[mid_b][mid_s] = 0

	# Print out the board
	def print_board(self):
		print()
		print("   a b c d e f g h")
		print("   _______________")
		for i in range(self.size):
			print(i + 1, "|", end="")
			for j in range(self.size):
				if (self.b[i][j] == self.blank):
					print(self.b[i][j], end = " ")
				else:
					print(self.colour[self.b[i][j]], end = " ")
			print()
		print()

	# Check if the game is over
	def over(self):
		if self.turn == self.max_turn:
			return True
		if len(self.find_valid(0)) == 0 or len(self.find_valid(1)) == 0:
			return True
		whites = 0
		blacks = 0
		for y in range(self.size):
			whites += self.b[y].count(0)
			blacks += self.b[y].count(1)
		if whites == 0 or blacks == 0:
			return True
		return False

	# Return the number of white and black squares
	def find_score(self):
		score = {self.colour[0]: 0, self.colour[1]: 0}
		for y in range(self.size):
			for x in range(self.size):
				if self.b[y][x] == 0:
					score[self.colour[0]] += 1
				elif self.b[y][x] == 1:
					score[self.colour[1]] += 1
		return score

	# Register the player's chosen location on the board
	def go(self, y, x, player):
		curr_colour = player
		oth_colour = (player + 1) % 2
		self.b[y][x] = curr_colour
		flip_dirs = self.find_flips(y, x, oth_colour, curr_colour)[0]
		for dir_index in flip_dirs:
			for mul in range(1, self.size):
				nY = y + mul * self.dy[dir_index]
				nX = x + mul * self.dx[dir_index]
				if not self.in_lim(nY, nX) or self.b[nY][nX] == curr_colour:
					break
				self.b[nY][nX] = curr_colour
		self.turn += 1

	# Check if a location is in the board
	def in_lim(self, y, x):
		return not (y < 0 or y >= self.size or x < 0 or x >= self.size)

	# Finds all valid locations for a player
	def find_valid(self, player):
		valid_moves = []
		for y in range(self.size):
			for x in range(self.size):
				if self.valid(y, x, player):
					valid_moves.append((y, x))
		return valid_moves

	# Check if a square is valid
	def valid(self, y, x, player):
		if self.b[y][x] != self.blank:
			return 0
		oth_player = (player + 1) % 2
		flip_dirs, flipped = self.find_flips(y, x, oth_player, player)
		return flipped

	# Find which direction a move flips, and how many it flips
	def find_flips(self, y, x, oth_player, player):
		flipped = 0
		flip_dirs = []
		for dir_index in range(len(self.dx)):
			if not self.in_lim(y + self.dy[dir_index], x + self.dx[dir_index]):
				continue
			if self.b[y + self.dy[dir_index]][x + self.dx[dir_index]] == oth_player:
				curr_flipped = 0
				for mul in range(1, self.size):
					nY = y + mul * self.dy[dir_index]
					nX = x + mul * self.dx[dir_index]
					if not self.in_lim(nY, nX) or self.b[nY][nX] == self.blank:
						break
					if self.b[nY][nX] == player:
						flip_dirs.append(dir_index)
						flipped += curr_flipped
						break
					curr_flipped += 1
		return flip_dirs, flipped