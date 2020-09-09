# Contains the code for implementation of reversi
# AI is currently a greedy algorithm which aims to flip the most squares
# REPLACED "B" WITH "." FOR VISIBILTY

# Currently the weights is predefined, hopefully can make an algo to determine
colour = ["W", "."]
dy = [1, 1, 0, -1, -1, -1, 0, 1]
dx = [0, 1, 1, 1, 0, -1, -1, -1]
weights = [
	[100, -50,  10,   5,   5,  10, -50, 100],
	[-50, -50,  -5,  -5,  -5,  -5, -50, -50],
	[ 10,  -5,  15,   0,   0,  15,  -5,  10],
	[  5,  -5,   0,   0,   0,   0,  -5,   5],
	[  5,  -5,   0,   0,   0,   0,  -5,   5],
	[ 10,  -5,  15,   0,   0,  15,  -5,  10],
	[-50, -50,  -5,  -5,  -5,  -5, -50, -50],
	[100,  10,  10,   5,   5,  10, -50, 100],
]


# Object to contain game data and methods
###############################################################################
class Game(object):
	def __init__(self):
		self.b = [["_" for j in range(8)] for i in range(8)]
		self.flip = [[[] for i in range(8)] for j in range(8)]
		self.turn = 0
		self.b[3][3] = colour[0]
		self.b[4][4] = colour[0]
		self.b[3][4] = colour[1]
		self.b[4][3] = colour[1]

	# Print out the board
	def print_board(self):
		print()
		print("   a b c d e f g h")
		print("   _______________")
		for i in range(8):
			print(i + 1, "|", end="")
			for j in range(8):
				print(self.b[i][j], end=" ")
			print()
		print()

	# Check if a square is valid
	def valid(self, y, x, player):
		if self.b[y][x] != "_":
			return 0
		curr_colour = colour[player]
		oth_colour = colour[(player + 1) % 2]
		self.flip[y][x] = []
		flipped = 0
		for i in range(8):
			if not self.in_limits(y + dy[i], x + dx[i]):
				continue
			if self.b[y + dy[i]][x + dx[i]] == oth_colour:
				curr_flipped = 0
				for j in range(1, 8):
					nY = y + j * dy[i]
					nX = x + j * dx[i]
					if not self.in_limits(nY, nX):
						break
					if self.b[nY][nX] == curr_colour:
						self.flip[y][x].append(i)
						flipped += curr_flipped
						break
					curr_flipped += 1
		return flipped

	# Check if the game is over
	def over(self):
		if self.turn == 64:
			return True
		whites = 0
		blacks = 0
		for y in range(8):
			whites += self.b[y].count(colour[0])
			blacks += self.b[y].count(colour[1])
		if whites == 0 or blacks == 0:
			return True
		return False

	# Register the player's chosen location on the board
	def go(self, y, x, player):
		new_colour = colour[player]
		self.b[y][x] = new_colour
		for i in self.flip[y][x]:
			for j in range(1, 8):
				nY = y + j * dy[i]
				nX = x + j * dx[i]
				if not self.in_limits(nY, nX) or self.b[nY][nX] == new_colour:
					break
				self.b[nY][nX] = new_colour

	# Check if a location is in the board
	def in_limits(self, y, x):
		return not (y < 0 or y > 7 or x < 0 or x > 7)

	# Return the number of white and black squares
	def find_score(self):
		score = {colour[0]: 0, colour[1]: 0}
		for i in range(8):
			for j in range(8):
				if self.b[i][j] == colour[0]:
					score[colour[0]] += 1
				elif self.b[i][j] == colour[1]:
					score[colour[1]] += 1
		return score


# Driver code + code to take human input
###############################################################################
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
			greedy(game, player)
		game.print_board()
		print(game.find_score())
		game.turn += 1
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
		print("Invalid location", loc)
	return y, x


# Ai code
###############################################################################
def greedy(game, player):
	moves = []
	for y in range(8):
		for x in range(8):
			flips = game.valid(y, x, player)
			if flips:
				moves.append({"y": y, "x": x, "flips": flips + weights[y][x]})
	moves.sort(key = lambda x:x["flips"], reverse = True)
	best = moves[0]
	game.go(best["y"], best["x"], player)


if __name__ == "__main__":
	main()
