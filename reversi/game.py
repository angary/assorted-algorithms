from copy import copy, deepcopy

class Game(object):

	def __init__(self, player = 0):
		self.turn = 0
		self.p = player
		self.offset = 0
		self.blank = "_"
		self.colour = ["W", "."]
		self.dy = [1, 1, 0, -1, -1, -1, 0, 1]
		self.dx = [0, 1, 1, 1, 0, -1, -1, -1]
		self.b = [[self.blank for j in range(8)] for i in range(8)]
		self.b[3][3] = self.b[4][4] = 0
		self.b[3][4] = self.b[4][3] = 1
		self.move_stack = [deepcopy(self.b)]
		self.player_stack = [player]

	# Print out the board
	def print_board(self):
		print()
		print("   a b c d e f g h")
		print("   _______________")
		for i in range(8):
			print(i + 1, "|", end="")
			for j in range(8):
				if (self.b[i][j] == self.blank):
					print(self.blank, end = " ")
				else:
					print(self.colour[self.b[i][j]], end = " ")
			print()
		print()

	# Check if the game is over
	def over(self):
		if self.turn == 60:
			return True
		score = self.find_score()
		if score[self.colour[0]] == 0 or score[self.colour[1]] == 0:
			return True
		if len(self.find_valid(0)) == 0 and len(self.find_valid(1)) == 0:
			return True
		return False

	# Return the number of white and black squares
	def find_score(self):
		score = {self.colour[0]: 0, self.colour[1]: 0}
		for y in range(8):
			score[self.colour[0]] += self.b[y].count(0)
			score[self.colour[1]] += self.b[y].count(1)
		return score

	# Register the player's chosen location on the board
	def go(self, y, x):
		oth_player = (self.p + 1) % 2
		self.b[y][x] = self.p
		self.flip_squares(y, x, oth_player)
		self.turn += 1
		if not self.find_valid(oth_player):
			self.offset += 1
			pass
		self.p = (self.turn + self.offset) % 2
		self.move_stack.append(deepcopy(self.b))
		self.player_stack.append(self.p)

	# Undo a move
	def undo(self):
		if self.turn > 0:
			print("Undoing the move")
			oth_player = self.player_stack[-1]
			while self.player_stack[-1] == oth_player:
				self.turn -= 1
				del self.move_stack[-1]
				del self.player_stack[-1]
			self.turn -= 1
			del self.move_stack[-1]
			del self.player_stack[-1]
			self.b = deepcopy(self.move_stack[-1])
			self.p = self.player_stack[-1]
		else:
			print("Cannot undo, no more previous moves")

	# Flip over the squares on the board
	def flip_squares(self, y, x, oth_player):
		flip_dirs = self.find_flips(y, x, oth_player, self.p)[0]
		for direc in flip_dirs:
			for mul in range(1, 8):
				nY = y + mul * self.dy[direc]
				nX = x + mul * self.dx[direc]
				if not self.in_lim(nY, nX) or self.b[nY][nX] == self.p:
					break
				self.b[nY][nX] = self.p

	# Check if a location is in the board
	def in_lim(self, y, x):
		return not (y < 0 or y >= 8 or x < 0 or x >= 8)

	# Finds all valid locations for a player
	def find_valid(self, player):
		valid_moves = []
		for y in range(8):
			for x in range(8):
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
		for dir_index in range(8):
			if not self.in_lim(y + self.dy[dir_index], x + self.dx[dir_index]):
				continue
			if self.b[y + self.dy[dir_index]][x + self.dx[dir_index]] == oth_player:
				curr_flipped = 0
				for mul in range(1, 8):
					nY = y + mul * self.dy[dir_index]
					nX = x + mul * self.dx[dir_index]
					if not self.in_lim(nY, nX) or self.b[nY][nX] == "_":
						break
					if self.b[nY][nX] == player:
						flip_dirs.append(dir_index)
						flipped += curr_flipped
						break
					curr_flipped += 1
		return flip_dirs, flipped