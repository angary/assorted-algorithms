# Pretty scuffed
# Currently only implements the game reversi without AI


dy = [1, 1, 0, -1, -1, -1, 0, 1]
dx = [0, 1, 1, 1, 0, -1, -1, -1]
colour = ["W", "B"]


class Game(object):
	def __init__(self):
		self.b = [["_" for j in range(8)] for i in range(8)]
		self.b[3][3] = "W"
		self.b[4][4] = "W"
		self.b[3][4] = "B"
		self.b[4][3] = "B"
		self.flip = []

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

	def valid(self, y, x, player):
		if self.b[y][x] != "_":
			return False
		curr_colour = colour[player]
		oth_colour = colour[(player + 1) % 2]
		self.flip = []
		for i in range(8):
			if not self.in_limits(y + dy[i], x + dx[i]):
				continue
			if self.b[y + dy[i]][x + dx[i]] == oth_colour:
				for j in range(1, 8):
					nY = y + j * dy[i]
					nX = x + j * dx[i]
					if not self.in_limits(nY, nX):
						break
					if self.b[nY][nX] == curr_colour:
						self.flip.append(i)
						break
		return (len(self.flip) > 0)

	def won(self):
		for i in range(8):
			if "_" in self.b[i]:
				return False
		return True

	def go(self, y, x, player):
		new_colour = colour[player]
		self.b[y][x] = new_colour
		for i in self.flip:
			for j in range(1, 8):
				nY = y + j * dy[i]
				nX = x + j * dx[i]
				if not self.in_limits(nY, nX) or self.b[nY][nX] == new_colour:
					break
				self.b[nY][nX] = new_colour

	def in_limits(self, y, x):
		return not (y < 0 or y > 7 or x < 0 or x > 7)

	def find_score(self):
		score = {"W": 0, "B": 0}
		for i in range(8):
			for j in range(8):
				if self.b[i][j] == "W":
					score["W"] += 1
				elif self.b[i][j] == "B":
					score["B"] += 1
		return score


def main():
	print("Game started")
	print("Enter positions as <letter><number>, i.e. a1")
	game = Game()
	turn = 1
	game.print_board()
	while not game.won():
		y, x = take_turn(game, turn)
		game.go(y, x, turn % 2)
		game.print_board()
		turn += 1
	print("Game over")
	game.print_board()
	print(game.find_score())


def take_turn(game, turn):
	while True:
		print("Currently", colour[turn % 2])
		loc = input("Choose position: ")
		x, y = int(ord(loc[0].lower()) - int(ord('a'))), int(loc[1]) - 1
		if game.in_limits(y, x) and game.valid(y, x, turn % 2):
			break
		print("Invalid location", loc)
	return y, x


if __name__ == "__main__":
	main()