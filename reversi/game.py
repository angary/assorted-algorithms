from copy import deepcopy
from colorama import Fore, Back, Style

BLANK = 2
COLOUR = ["O", "X", " "]
DY = [1, 1, 0, -1, -1, -1, 0, 1]
DX = [0, 1, 1, 1, 0, -1, -1, -1]
DIRECTIONS = 8
SIZE = 8

class Game(object):
    def __init__(self, player: int = 0):
        self.turn = 0
        self.p = player
        self.offset = 0
        self.b = [[BLANK] * SIZE for _ in range(SIZE)]
        self.b[3][3] = self.b[4][4] = 0
        self.b[3][4] = self.b[4][3] = 1
        self.move_stack = [deepcopy(self.b)]
        self.player_stack = [player]

    # Print out the board
    def print_board(self) -> None:
        print()
        print("   a b c d e f g h")
        print("   ________________")
        for i in range(SIZE):
            print(i + 1, "|", end="")
            for j in range(SIZE):
                print(Back.GREEN, end="")
                if self.b[i][j] == 0:
                    print(Fore.WHITE + COLOUR[0], end=" ")
                elif self.b[i][j] == 1:
                    print(Fore.BLACK + COLOUR[1], end=" ")
                else:
                    print(COLOUR[2], end=" ")
                print(Style.RESET_ALL, end="")
            print()
        print()

    # Check if the game is over
    def over(self) -> bool:
        if self.turn == 60:
            return True
        return self.find_valid(0) + self.find_valid(1) == []

    # Return the number of white and black squares
    def find_score(self) -> dict[str, int]:
        colour_0 = sum([self.b[y].count(0) for y in range(SIZE)])
        return {
            COLOUR[0]: colour_0,
            COLOUR[1]: self.turn + 4 - colour_0
        }

    # Register the player's chosen location on the board
    def go(self, y: int, x: int) -> None:
        oth_player = (self.p + 1) % 2
        self.b[y][x] = self.p
        self.flip_squares(y, x, oth_player)
        self.turn += 1
        if not self.find_valid(oth_player):
            self.offset += 1
        self.p = (self.turn + self.offset) % 2
        self.move_stack.append(deepcopy(self.b))
        self.player_stack.append(self.p)

    # Undo a move
    def undo(self) -> None:
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
    def flip_squares(self, y: int, x: int, oth_player: int) -> None:
        flip_dirs = self.find_flips(y, x, oth_player, self.p)['flip_dirs']
        for direc in flip_dirs:
            for mul in range(1, SIZE):
                nY = y + mul * DY[direc]
                nX = x + mul * DX[direc]
                if not self.in_lim(nY, nX) or self.b[nY][nX] == self.p:
                    break
                self.b[nY][nX] = self.p

    # Check if a location is in the board
    def in_lim(self, y: int, x: int) -> bool:
        return (0 <= y < SIZE and 0 <= x < SIZE)

    # Finds all valid locations for a player
    def find_valid(self, player: int) -> list[tuple[int, int]]:
        return [
            (y, x) for y in range(SIZE) for x in range(SIZE) if self.valid(y, x, player)
        ]

    # Return how many squares that position can flip
    def valid(self, y: int, x: int, player: int) -> int:
        if self.b[y][x] != BLANK:
            return 0
        oth_player = (player + 1) % 2
        return self.find_flips(y, x, oth_player, player)['flipped_count']

    # Find which direction a move flips, and how many it flips
    def find_flips(self, y: int, x: int, oth_player: int, player: int) -> dict:
        flipped_count = 0
        flip_dirs = []
        for direction in range(DIRECTIONS):
            nY = y + DY[direction]
            nX = x + DX[direction]
            if self.in_lim(nY, nX) and self.b[nY][nX] == oth_player:
                for curr_flipped in range(SIZE):
                    if not self.in_lim(nY, nX) or self.b[nY][nX] == BLANK:
                        break
                    if self.b[nY][nX] == player:
                        flip_dirs.append(direction)
                        flipped_count += curr_flipped
                        break
                    nY += DY[direction]
                    nX += DX[direction]
        return {'flip_dirs': flip_dirs, 'flipped_count': flipped_count}
