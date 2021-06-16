import math
import copy
from reversi import checked

# Global variables because I'm lazy
transposition_table = {}


# Actual AI algorithm (Algos code)
################################################################################
# Main code
def minimax(g, priority, alpha, beta, depth):

    if g.over() or depth == 0:
        return find_score(g, priority)

    valid_moves = heuristic_sort(g, g.find_valid(g.p))
    best_y, best_x = valid_moves[0]
    best_eval = -math.inf if g.p == priority else math.inf

    for y, x in valid_moves:
        new = copy.deepcopy(g)
        new.go(y, x)
        new_eval = minimax(new, priority, alpha, beta, depth - 1)
        new_eval = new_eval[0]
        if g.p == priority:
            if new_eval > best_eval:
                best_eval = new_eval
                best_y = y
                best_x = x
            alpha = max(alpha, best_eval)
        else:
            if new_eval < best_eval:
                best_eval = new_eval
                best_y = y
                best_x = x
            beta = min(beta, best_eval)
        if beta <= alpha:
            break
    return best_eval, best_y, best_x


# Sort moves according to which one seems better
def heuristic_sort(g, valid_moves):
    sorted_moves = []
    for move in valid_moves:
        y, x = move
        new = copy.deepcopy(g)
        new.go(y, x)
        rating = heuristic_score(new, g.p)
        sorted_moves.append({"move": move, "rating": rating})
    sorted_moves.sort(key=lambda x: x["rating"], reverse=True)
    return [move["move"] for move in sorted_moves]


# Finds the score of the baord
def find_score(g, priority):
    key = zobrist_key(g)
    if key[0] in transposition_table:
        if key[1] in transposition_table[key[0]]:
            score = transposition_table[key[0]][key[1]]
        else:
            score = heuristic_score(g, priority)
            transposition_table[key[0]][key[1]] = score
    else:
        score = heuristic_score(g, priority)
        transposition_table[key[0]] = {}
        transposition_table[key[0]][key[1]] = score
    return (score, -1, -1)


# Generates a zobrist key for the board
def zobrist_key(g):
    shift = 1
    key0 = 0
    key1 = 0
    for y in range(8):
        for x in range(8):
            if g.b[y][x] == 0:
                key0 += shift
            elif g.b[y][x] == 1:
                key1 += shift
            shift *= 2
    return (key0, key1)


# AI Heuristic (Maths code)
################################################################################
# Score the game using the heuristic
def heuristic_score(g, player):
    rating = 0
    oth_player = (player + 1) % 2

    # Each of these score functions will retrun a value out of 100
    # A bigger value = better for the player
    mobility = mobility_score(g, player, oth_player)
    corner = corner_score(g, player, oth_player)
    frontier = frontier_score(g, player, oth_player)
    weight = weight_score(g, player, oth_player)
    stability = stability_score(g, player, oth_player)

    # Corners are always weighted highly
    rating += 2 * corner

    # We prioritise having a low frontier and high mobility early on,
    # but later on as we cover more squares, our frontier will increase, and
    # our mobility drops, so we weigh the values less
    rating += 2 * (1 - (g.turn / 60)) * frontier
    rating += 2 * (1 - (g.turn / 60)) * mobility

    # Early on, the number of squares we control, isn't too important, as we can
    # flip more later on. However, towards the lategame, we value this more.
    rating += 2 * (1 + (g.turn / 60)) * stability
    rating += 2 * (1 + (g.turn / 60)) * weight

    # Returns a weighting out of 1000
    return rating


# Determine if the current player has better mobility
def mobility_score(g, player, oth_player):
    my_mobility = len(g.find_valid(player))
    oth_mobility = len(g.find_valid(oth_player))
    total_mobility = my_mobility + oth_mobility
    return (my_mobility - oth_mobility) / max(total_mobility, 1)


# Find how many corner player owns compared to other player
def corner_score(g, player, oth_player):
    corners = [0, 0]
    if g.b[0][0] != g.blank:
        corners[g.b[0][0]] += 1
    if g.b[7][0] != g.blank:
        corners[g.b[7][0]] += 1
    if g.b[0][7] != g.blank:
        corners[g.b[0][7]] += 1
    if g.b[7][7] != g.blank:
        corners[g.b[7][7]] += 1
    return (corners[player] - corners[oth_player]) / max(sum(corners), 1)


# Check number of the squares on the player's frontier
def frontier_score(g, player, oth_player):
    visited = [[[False] * 8 for j in range(8)] for i in range(2)]
    frontier = [0, 0]
    for y in range(8):
        for x in range(8):
            if g.b[y][x] != g.blank:
                curr_player = g.b[y][x]
                for i in range(8):
                    nY = y + g.dy[i]
                    nX = x + g.dx[i]
                    if (g.in_lim(nY, nX) and g.b[nY][nX] != curr_player
                            and visited[curr_player][nY][nX] == False):
                        visited[curr_player][nY][nX] = True
                        frontier[curr_player] += 1
    return (frontier[oth_player] - frontier[player]) / max(sum(frontier), 1)


# Calculate the value of the board based on predetermined weights
def weight_score(g, player, oth_player):
    weights = [0, 0]
    for y in range(8):
        for x in range(8):
            if g.b[y][x] != g.blank:
                weights[g.b[y][x]] += square_weight(g, y, x)
    sum_weights = 1 if sum(weights) == 0 else sum(weights)
    return (weights[player] - weights[oth_player]) / sum_weights


# Calculate how hard it is for a player to change the configuration of the board
def stability_score(g, player, oth_player):
    stabils = [0, 0]
    for y in range(8):
        for x in range(8):
            if g.b[y][x] != g.blank:
                stabils[g.b[y][x]] += square_stabil(g, y, x)
    return (stabils[player] - stabils[oth_player]) / max(sum(stabils), 1)


# Heuristic Utils
################################################################################
# Find the stability of a square
def square_stabil(g, y, x):
    opposition = (g.b[y][x] + 1) % 2

    stability = 128
    oppositions = [False] * 8
    blanks = [0] * 8

    # Check every direction along current square's row, column, and diagonals
    for dir in range(8):
        nY = y
        nX = x

        # Check every square in current direction
        for _ in range(8):
            nY += g.dy[dir]
            nX += g.dx[dir]

            # If it is still within the board
            if g.in_lim(nY, nX):

                # If the new square is blank
                if g.b[nY][nX] == g.blank:
                    blanks[dir] += 1

                # If not blanks yet found in this direction and
                # the current square is of the other player
                if blanks[dir] == 0 and g.b[nY][nX] == opposition:
                    oppositions[dir] == True
            else:
                break

    # Double stability if square cannot be immediately flipped in a direction
    for dir in range(8):

        # If oth player on one side, and on the other side, there is free square
        opp_dir = (dir + 4) % 8
        if oppositions[dir] and not oppositions[opp_dir] and blanks[opp_dir]:
            stability >>= 3
        else:
            stability <<= 1

    # If there are more blanks along one side, a square is more unstable
    for dir in range(4):
        min_blank = min(blanks[dir], blanks[dir + 4])
        if min_blank % 2 == 0:
            stability <<= 1
        else:
            stability >>= 1
        # stability >>= (blanks[dir] * blanks[dir + 4]) >> 1

    if x % 2 == 0 and y % 2 == 0:
        stability <<= 2
    elif x % 2 == 1 and y % 2 == 1:
        stability >>= 1

    return stability


# Find the weight/ value of a square
def square_weight(g, y, x):
    weight = 0

    # Find the distance of current coordinate from center
    x_dist = 4 - x if x < 4 else x - 3
    y_dist = 4 - y if y < 4 else y - 3
    x_weight = 2 << x_dist
    y_weight = 2 << y_dist

    # Weight good if distance from center even, else bad, because if even,
    # it can be flipped, then flipped back, more importantly, parity determines
    # if piece can take or give a corner. This effect increases with distance
    # from center as outer even squares more valuable, whereas odd bad
    # as it gives opponent opportunity to take good squares
    weight = weight + x_weight if x_dist % 2 == 0 else weight - x_weight
    weight = weight + y_weight if y_dist % 2 == 0 else weight - y_weight
    if x_dist % 2 == 0 and y_dist % 2 == 0:
        weight <<= 2
    elif x_dist % 2 == 1 and y_dist % 2 == 1:
        weight >>= 2

    corner = near_corner(g, y, x)
    if corner:
        if g.b[corner['y']][corner['x']] == g.b[y][x]:
            weight = 64
    return weight


# Check if a square is one piece away from a corner
def near_corner(g, y, x):
    for i in range(8):
        if is_corner(y + g.dy[i], x + g.dx[i]):
            return {'y': y + g.dy[i], 'x': x + g.dx[i]}
    return False


# Check if a square is a corner
def is_corner(y, x):
    if (y == 0 or y == 7) and (x == 0 or x == 7):
        return True
    return False
