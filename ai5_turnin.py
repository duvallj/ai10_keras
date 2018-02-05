import pickle
import time
from collections import deque
from multiprocessing import Process, Value

import my_core
import Othello_Core as oc

sq = oc.OthelloCore().squares()

def load_matrix(filename):
    try:
        file = open(filename, 'rb')
        mtrx = pickle.load(file)
        file.close()
        return mtrx
    except (FileNotFoundError, EOFError):
        return dict()


def write_matrix(matrix, filename):
    file = open(filename, 'wb')
    pickle.dump(matrix, file)
    file.close()


mcore = my_core.MyCore()
tMatrix = {11: (12, [], 0), 12: (-2, [11], 2.5), 13: (2, [12, 14], 2.2), 14: (0.5, [13, 15], 0.7), 15: (0.5, [14, 16], 0.7), 16: (2, [15, 17], 2.2), 17: (-2, [18], 2.5), 18: (12, [], 0), 21: (-2, [11], 2.5), 22: (-4, [11, 12, 21], 4.5), 23: (-0.5, [12, 13, 14], 0.8), 24: (-0.5, [13, 14, 15], 0.8), 25: (-0.5, [14, 15, 16], 0.8), 26: (-0.5, [15, 16, 17], 0.8), 27: (-4, [18, 17, 28], 4.5), 28: (-2, [18], 2.5), 31: (2, [21, 41], 2.2), 32: (-0.5, [21, 31, 41], 0.8), 33: (1.5, [], 0), 34: (0.3, [], 0), 35: (0.3, [], 0), 36: (1.5, [], 0), 37: (-0.5, [28, 38, 48], 0.8), 38: (2, [28, 48], 2.2), 41: (0.5, [31, 51], 0.7), 42: (-0.5, [31, 41, 51], 0.8), 43: (0.3, [], 0), 44: (0.3, [], 0), 45: (0.3, [], 0), 46: (0.3, [], 0), 47: (-0.5, [38, 48, 58], 0.8), 48: (0.5, [38, 58], 0.7), 51: (0.5, [41, 61], 0.7), 52: (-0.5, [41, 51, 61], 0.8), 53: (0.3, [], 0), 54: (0.3, [], 0), 55: (0.3, [], 0), 56: (0.3, [], 0), 57: (-0.5, [48, 58, 68], 0.8), 58: (0.5, [48, 68], 0.7), 61: (2, [51, 71], 2.2), 62: (-0.5, [51, 61, 71], 0.8), 63: (1.5, [], 0), 64: (0.3, [], 0), 65: (0.3, [], 0), 66: (1.5, [], 0), 67: (-0.5, [58, 68, 78], 0.8), 68: (2, [58, 78], 2.2), 71: (-2, [81], 2.5), 72: (-4, [81, 82, 78], 4.5), 73: (-0.5, [82, 83, 84], 0.8), 74: (-0.5, [83, 84, 85], 0.8), 75: (-0.5, [84, 85, 86], 0.8), 76: (-0.5, [85, 86, 87], 0.8), 77: (-4, [88, 78, 87], 4.5), 78: (-2, [88], 2.5), 81: (12, [], 0), 82: (-2, [81], 2.5), 83: (2, [82, 84], 2.2), 84: (0.5, [83, 85], 0.7), 85: (0.5, [84, 86], 0.7), 86: (2, [85, 87], 2.2), 87: (-2, [88], 2.5), 88: (12, [], 0)}
#tMatrix=load_matrix('C:/Users/Me/Documents/AI/othello/nmatrix.pkl')


# tDict = loadMatrix('C:/Users/Me/Documents/AI/othello/lookupdict.pkl')
class Strategy(my_core.MyCore):
    def best_strategy(self, board, player, move, flag):
        move.value = iterdepthlimited(player, board, mcore, flag, tMatrix)  # , tDict)


def ai_strategy_nonshared(player, board, core, conn):
    move = Value('i', 0)
    flag = Value('H', 0)
    proc = Process(target=ai_strategy, args=(player, board, move, flag))
    proc.start()
    time.sleep(10)
    flag.value = 1
    print('Flag sent?')
    proc.join(1)
    if proc.is_alive():
        proc.terminate()
        print('Process terminated forcefully')
    else:
        print('Process ended successfully')
    return move.value


def find_all_brackets(board, player, spots_left, core):
    brackets = {}
    for spot in spots_left:
        this_spot_brackets = {}
        for direction in oc.DIRECTIONS:
            bracket = core.find_bracket(spot, player, board, direction)
            if bracket is not None:
                this_spot_brackets[direction] = bracket
        if this_spot_brackets:
            brackets[spot] = this_spot_brackets
    return brackets


def gen_all_good_children(node, core, matrix, oplayer):  # , lookupdict):
    # We can't generate children if it is an end-case
    if len(node[3]) == 0:
        return

    # elif node[9] in lookupdict:
    #    for x in range(9):
    #        node[x] = lookupdict[node[9]][x]
    else:

        for spot in node[6]:
            nboard = node[1].copy()
            for direction in node[6][spot]:
                for flipspot in range(spot, node[6][spot][direction], direction):
                    nboard[flipspot] = node[2]

            nspots_left = node[3] - {spot}
            oppo = core.opponent(node[2])
            brackets = find_all_brackets(nboard, oppo, nspots_left, core)

            nscore = score(nboard, oplayer, core, matrix, len(brackets))

            # If we can't make a move
            if len(brackets) == 0:

                # Try the original player again
                oppo = node[2]
                brackets = find_all_brackets(nboard, oppo, nspots_left, core)

                if len(brackets) == 0:
                    # If they still can't make a move, score the board
                    mcount = nboard.count(oplayer)
                    ocount = nboard.count(core.opponent(oplayer))

                    # 335.2 is the maximum score weighted
                    if mcount > ocount:
                        nscore = 335.2 - ocount
                    elif ocount > mcount:
                        nscore = mcount - 335.2
                    else:
                        nscore = 0
                    nspots_left = set()

            node[4].append(
                [nscore, nboard, oppo, nspots_left, [], node, brackets, spot, -1])  # , oppo+''.join(nboard)])

            # lookupdict[node[9]] = node


def sortfunc(x):
    return x[0]


def propragonate_minimax(leaf, oplayer):
    # Like regular minimax, but bottom-up
    node = leaf
    while node is not None:
        if len(node[4]) > 0:
            if oplayer == node[2]:
                bchild = max(node[4], key=sortfunc)
            else:
                bchild = min(node[4], key=sortfunc)

            # Right here is one of the only reasons I can't use tuples
            node[0] = bchild[0]
            node[8] = bchild[7]
        node = node[5]


def iterdepthlimited(player, board, core, flag, matrix):  # , lookdict):
    start_time = time.time()
    going = True
    spots_left = set(x for x in sq if board[x] == oc.EMPTY)
    root = [0, board, player, spots_left, [], None, find_all_brackets(board, player, spots_left, core), -1,
            -1]  # , player+''.join(board)]
    # Node structure:
    # * 0 = score
    # * 1 = board
    # * 2 = player
    # * 3 = spots left
    # * 4 = children nodes
    # * 5 = parent node
    # * 6 = brackets (only legal moves)
    # * 7 = prev move
    # * 8 = best move
    # * 9 = condensed board w/ player (for lookups)
    queue = deque([root])
    depth = 0
    while going:
        nqueue = deque()
        going = False
        while queue:
            going = True
            node = queue.pop()
            gen_all_good_children(node, core, matrix, player)  # , lookdict)
            nqueue.extend(node[4])
            propragonate_minimax(node, player)

            if flag.value==0:  # or depth >= maxdepth:
                going = False
                break

        queue = nqueue
        depth += 1
        print(depth)

    # print(root)
    end_time = time.time()
    print(end_time - start_time)
    return root[8]


def print_matrix(matrix):
    for y in range(1, 9):
        for x in range(1, 9):
            print(str(matrix[y * 10 + x][0]).rjust(5), end='')
        print()


similars = [[11, 18, 81, 88],
            [12, 21, 17, 71, 28, 82, 78, 87],
            [13, 31, 16, 61, 38, 83, 68, 86],
            [14, 41, 15, 51, 48, 84, 58, 85],
            [22, 27, 72, 77],
            [23, 32, 26, 62, 73, 37, 76, 67],
            [24, 42, 25, 52, 74, 47, 75, 57],
            [33, 36, 63, 66],
            [34, 43, 35, 53, 64, 46, 65, 56],
            [44, 45, 54, 55]
            ]


def score(board, player, core, matrix, nmoves):
    # matrix notation:
    # dict of all elements in sq, for each element:
    # 3-tuple
    #  0: amnt of points that place is usually worth
    #  1: set of spots that need to be non empty in order for
    #  2: amnt of points if requirements in 1 are ment
    oppo = core.opponent(player)
    cscore = 0
    mcount = 0
    ocount = 0
    for spot in sq:
        regular, req, special = matrix[spot]
        if board[spot] == player:
            if req and all(board[x] != oc.EMPTY for x in req):
                cscore += special
            else:
                cscore += regular
            mcount += 1
        elif board[spot] == oppo:
            if req and all(board[x] != oc.EMPTY for x in req):
                cscore -= special
            else:
                cscore -= regular
            ocount += 1
    if mcount + ocount == 64:
        if mcount > ocount:
            return 335.2 - ocount
        elif ocount > mcount:
            return mcount - 335.2
        else:
            return 0
    else:
        return cscore * (1 / (nmoves + 1) + 1)
