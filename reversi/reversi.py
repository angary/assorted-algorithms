# Contains the code for implementation of reversi and minimax AI
# REPLACED "B" WITH "." FOR VISIBILTY
# TODO:
# - Iterative deepening
# - Principal variation search

from game import Game
from computer import *
import math
import time

# Global variable to check how many scenarios the algo checked
# just exists for testing
checked = 0


# Driver code
################################################################################
def main():
	g = Game()
	print("Game started")
	print("Enter positions as <letter><number>, i.e. a1")
	g.print_board()
	start_time = time.time()
	
	# Depth for minimax search
	depth = int(input("Depth of minimax search: "))

	while not g.over():

		# Take input
		curr = checked
		if g.p == 0: 
			computer_turn(g, depth)
			# human_turn(g, g.p)
		else:
			computer_turn(g, depth)
		
		# Print out values
		print("Player is", g.p)
		g.print_board()
		print(g.find_score())
		print("Turn is", g.turn, "\ttotal:", checked, "\tprev:", checked - curr)

		if g.turn > 50:
			depth += 1

	# Game over
	print("Checked:", checked)
	print("Game over")
	print("Time taken: {}".format(time.time() - start_time))
	g.print_board()
	print(g.find_score())


# Input code
################################################################################
# Take the input from human player
def human_turn(g, player):
	while True:
		print("Currently", g.colour[player])
		try:
			loc = input("Choose position: ").strip()
			if loc == "u" or loc == "U":
				g.undo()
				return
			else:
				x, y = int(ord(loc[0].lower()) - int(ord('a'))), int(loc[1]) - 1
				if g.in_lim(y, x) and g.valid(y, x, player):
					g.go(y, x)
					return
				print("Invalid location:", loc)
		except:
			print("Invalid input")


# Take the computer's turn
def computer_turn(g, depth):
	best = minimax(g, g.p, -math.inf, math.inf, depth)
	g.go(best[1], best[2])


if __name__ == "__main__":
	main()