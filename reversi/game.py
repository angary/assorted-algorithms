class Game(object):

	def __init__(self, size = 8, player = 0):
		self.size = size
		self.turn = 0
		self.player = player
		self.offset = 0
		self.max_turn = (size ** 2) - 4
		self.blank = "_"
		self.colour = ["W", ".", "_"]
		self.dy = [1, 1, 0, -1, -1, -1, 0, 1]
		self.dx = [0, 1, 1, 1, 0, -1, -1, -1]
		self.b = [[self.blank for j in range(size)] for i in range(size)]
		self.setup_board()
	
	# Set up first four squares
	def setup_board(self):
		mid_s = (self.size // 2) - 1
		mid_b = self.size // 2
		self.b[mid_s][mid_s] = self.b[mid_b][mid_b] = 0
		self.b[mid_s][mid_b] = self.b[mid_b][mid_s] = 1

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
		score = self.find_score()
		if score[self.colour[0]] == 0 or score[self.colour[1]] == 0:
			return True
		return False

	# Return the number of white and black squares
	def find_score(self):
		score = {self.colour[0]: 0, self.colour[1]: 0}
		for y in range(self.size):
			score[self.colour[0]] += self.b[y].count(0)
			score[self.colour[1]] += self.b[y].count(1)
		return score

	# Register the player's chosen location on the board
	def go(self, y, x, player):
		oth_colour = (player + 1) % 2
		self.b[y][x] = player
		flip_dirs = self.find_flips(y, x, oth_colour, player)[0]
		for dir in flip_dirs:
			for mul in range(1, self.size):
				nY = y + mul * self.dy[dir]
				nX = x + mul * self.dx[dir]
				if not self.in_lim(nY, nX) or self.b[nY][nX] == player:
					break
				self.b[nY][nX] = player
		self.turn += 1
		if not self.find_valid(oth_colour):
			self.offset += 1
		self.player = (self.turn + self.offset) % 2

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
		for dir in range(len(self.dx)):
			nY = y + self.dy[dir]
			nX = x + self.dx[dir]
			if (self.in_lim(nY, nX) and self.b[nY][nX] == oth_player):
				curr_flipped = 1
				for mul in range(self.size):
					nY += self.dy[dir]
					nX += self.dx[dir]
					if (self.in_lim(nY, nX) and (self.b[nY][nX] == player)):
						flip_dirs.append(dir)
						flipped += curr_flipped
						break
					curr_flipped += 1
		return flip_dirs, flipped