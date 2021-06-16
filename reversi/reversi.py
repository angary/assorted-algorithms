# Contains the code for implementation of reversi and minimax AI

from game import Game
from computer import *
from colorama import Fore, Back, Style
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
    option = input_wrapper(input_option)()

    # Depth for minimax search
    depth = 0
    if option >= 2:
        depth = input_wrapper(input_depth)()

    while not g.over():

        # Take input
        if g.p == 0:
            if option < 3:
                input_wrapper(human_turn(g, g.p))
            else:
                computer_turn(g, depth)
        else:
            if option % 2 == 1:
                input_wrapper(human_turn(g, g.p))
            else:
                computer_turn(g, depth)

        # Print out values
        print("Turn is", g.turn, "Player is", g.p)
        g.print_board()
        print(g.find_score())

    # Game over
    print("Game over")
    print("Time taken: {}".format(time.time() - start_time))
    g.print_board()
    print(g.find_score())


# Input code
################################################################################
# Adds wrapper to function to check for invalid inputs
def input_wrapper(func):
    def wrapper(*args):
        while True:
            try:
                input = func(*args)
                if input:
                    return input
            except:
                print(Fore.RED + "Invalid input" + Style.RESET_ALL)

    return wrapper


# Take playing option input
def input_option():
    print("Enter how you want the game to be played")
    option = int(
        input(
            "[1]: Human vs Human\n[2]: Human vs Computer\n[3]: Computer vs Human\n[4]: Computer vs Computer\n"
        ))
    if option > 0 and option < 5:
        return option
    print(Fore.RED + "Invalid option" + Style.RESET_ALL)


# Take depth of minimax search
def input_depth():
    depth = int(input("Enter depth of minimax search: "))
    if depth > 0:
        return depth
    print(Fore.RED + "Invalid depth" + Style.RESET_ALL)


# Take the input from human player
def human_turn(*args):
    g = args[0]
    player = args[1]
    print("Currently", g.colour[player])
    loc = input("Choose position: ").strip()
    if loc == "u" or loc == "U":
        g.undo()
        return True
    x, y = int(ord(loc[0].lower()) - int(ord('a'))), int(loc[1]) - 1
    if g.in_lim(y, x) and g.valid(y, x, player):
        g.go(y, x)
        return True
    print(Fore.RED + "Invalid choice" + Style.RESET_ALL)


# Take the computer's turn
def computer_turn(g, depth):
    best = minimax(g, g.p, -math.inf, math.inf, depth)
    g.go(best[1], best[2])


if __name__ == "__main__":
    main()
