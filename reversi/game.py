from copy import deepcopy
from colorama import Fore, Back, Style


class Game(object):
    def __init__(self, player=0):
        self.turn = 0
        self.p = player
        self.offset = 0
        self.blank = 2
        self.colour = ["O", "X", " "]
        self.dy = [1, 1, 0, -1, -1, -1, 0, 1]
        self.dx = [0, 1, 1, 1, 0, -1, -1, -1]
        self.b = [[self.blank] * 8 for _ in range(8)]
        self.b[3][3] = self.b[4][4] = 0
        self.b[3][4] = self.b[4][3] = 1
        self.move_stack = [deepcopy(self.b)]
        self.player_stack = [player]

    # Print out the board
    def print_board(self):
        print()
        print("   a b c d e f g h")
        print("   ________________")
        for i in range(8):
            print(i + 1, "|", end="")
            for j in range(8):
                print(Back.GREEN, end="")
                if self.b[i][j] == 0:
                    print(Fore.WHITE + self.colour[0], end=" ")
                elif self.b[i][j] == 1:
                    print(Fore.BLACK + self.colour[1], end=" ")
                else:
                    print(self.colour[2], end=" ")
                print(Style.RESET_ALL, end="")
            print()
        print()

    # Check if the game is over
    def over(self):
        if self.turn == 60:
            return True
        if len(self.find_valid(0)) == 0 and len(self.find_valid(1)) == 0:
            return True
        return False

    # Return the number of white and black squares
    def find_score(self):
        score = {self.colour[0]: 0, self.colour[1]: 0}
        for y in range(8):
            score[self.colour[0]] += self.b[y].count(0)
        score[self.colour[1]] = (self.turn + 4) - score[self.colour[0]]
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
        flip_dirs = self.find_flips(y, x, oth_player, self.p)['flip_dirs']
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

    # Return how many squares that position can flip
    def valid(self, y, x, player):
        if self.b[y][x] != self.blank:
            return 0
        oth_player = (player + 1) % 2
        return self.find_flips(y, x, oth_player, player)['flipped_count']

    # Find which direction a move flips, and how many it flips
    def find_flips(self, y, x, oth_player, player):
        flipped_count = 0
        flip_dirs = []
        for direction in range(8):
            nY = y + self.dy[direction]
            nX = x + self.dx[direction]
            if self.in_lim(nY, nX) and self.b[nY][nX] == oth_player:
                for curr_flipped in range(8):
                    if not self.in_lim(nY, nX) or self.b[nY][nX] == self.blank:
                        break
                    if self.b[nY][nX] == player:
                        flip_dirs.append(direction)
                        flipped_count += curr_flipped
                        break
                    nY += self.dy[direction]
                    nX += self.dx[direction]
        return {'flip_dirs': flip_dirs, 'flipped_count': flipped_count}
