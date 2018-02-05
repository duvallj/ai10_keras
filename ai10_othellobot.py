import numpy as np
from math import inf
#import ai5
import Othello_Core as oc
import my_core as mc
import pickle
import sys
from itertools import combinations_with_replacement
import ai10_consts as consts
sys.stdout.write('ai10 imported\n')


class Node:
    def __init__(self, a0, a1, a2, a3, a4, a5, a6):
        self.score = a0
        self.board = a1
        self.player = a2
        self.spots_left = a3
        self.parent = a4
        self.brackets = a5
        self.prev_move = a6
        self.children = []
        self.best_move = -1

def find_bracket(square, player, board, direction):
    current = square + direction
    opponent = player * -1
    inbetween = False

    while board[current] == opponent:
        current += direction
        inbetween = True

    toreturn = False

    if board[current] == player and inbetween:
        toreturn = current

    return toreturn

def find_all_brackets(board, player, spots_left):
    brackets = {}
    for spot in spots_left:
        this_spot_brackets = {}
        for direction in oc.DIRECTIONS:
            bracket = find_bracket(spot, player, board, direction)
            if bracket:
                this_spot_brackets[direction] = bracket
        if this_spot_brackets:
            brackets[spot] = this_spot_brackets
    return brackets

def relu(x):
    return (x > 0) * x

def logi(x):
    if x > -709:
        return 1/(1+np.exp(-x))
    else:
        return 0

def score(board, player, vals, nmoves):
    cscore = 0
    mcount = 0#board.count(player)
    ocount = 0#board.count(-player)
    
    for spot in consts.legal:
        s = board[spot]
        if s == player:
            mcount += 1
        elif s == -player:
            ocount += 1
    if mcount + ocount == 64:
        if mcount > ocount:
            return inf
        elif mcount < ocount:
            return -inf
        else:
            return 0

    vct = np.reshape(np.reshape(board, (10,10))[1:9, 1:9], (1, -1))
    layers = len(vals)
    logi_l = layers-1

    for l in range(layers):
        vct = (vct @ vals[l][0]) + vals[l][1]
        if l == logi_l:
            vct = logi(vct)
        else:
            vct = relu(vct)

    cscore = 128 * vct[0][0] - 64
    
    return cscore * (1 / (nmoves + 1) + 1) * player

def gen_all_good_children(node, matrix, oplayer):
    # We can't generate children if it is an end-case
    if len(node.spots_left) == 0:
        return
    elif not node.children:
        for spot in node.brackets:
            nboard = node.board.copy()
            for direction in node.brackets[spot]:
                for flipspot in range(spot, node.brackets[spot][direction], direction):
                    nboard[flipspot] = node.player

            nspots_left = node.spots_left - {spot}
            oppo = -node.player #core.opponent(node.player)
            brackets = find_all_brackets(nboard, oppo, nspots_left)

            nscore = 0 #score(nboard, oplayer, core, matrix, len(brackets))

            # If we can't make a move
            if len(brackets) == 0:

                # Try the original player again
                oppo = node.player
                brackets = find_all_brackets(nboard, oppo, nspots_left)

                if len(brackets) == 0:
                    # If they still can't make a move, score the board
                    mcount = 0
                    ocount = 0
                    for spot in consts.legal:
                        s = nboard[spot]
                        if s == oplayer:
                            mcount += 1
                        elif s == -oplayer:
                            ocount += 1

                    if mcount > ocount:
                        nscore = inf
                    elif ocount > mcount:
                        nscore = -inf
                    else:
                        nscore = 0
                    nspots_left = set()

            node.children.append(Node(nscore, nboard, oppo, nspots_left, node, brackets, spot))

def AlphaBeta(node, height, alpha, beta, matrix, oplayer, flag):
    if height == 0 or not flag.value:
        node.score = score(node.board, oplayer, matrix, len(node.brackets))
        #print(node.score, '\n', oc.OthelloCore().print_board(consts.ndarray2board(node.board)))
        return node.score, -1
    if len(node.spots_left) == 0:
        return node.score, -1
    
    max_val = alpha
    best_move = -1
    gen_all_good_children(node, matrix, oplayer)
    for child in node.children:
        if not flag.value:
            return max_val, best_move
        if child.player == node.player:
            val, temp = AlphaBeta(child, height-1, alpha, beta, matrix, oplayer, flag)
        else:
            val, temp = AlphaBeta(child, height-1, -beta, -max_val, matrix, oplayer, flag)
            val *= -1
        if val > max_val:
            if val >= beta: return val, child.prev_move
            max_val = val
            best_move = child.prev_move
        if best_move == -1:
            best_move = child.prev_move
            
    return max_val, best_move
#def MPC(node, height, alpha, beta, core, matrix, oplayer):
#    pass

class Strategy(mc.MyCore):
    def __init__(self):
        file = open("networkB.pkl", 'rb')
        self.tMatrix = pickle.load(file)
        self.players_d = {oc.BLACK: consts.BLACK, oc.WHITE: consts.WHITE}
        self.depthlist = (2, 3, 4, 5, 6, 7, 8, 10, 12, 15, 20, 25, 30)
        file.close()
        super().__init__()

    def best_strategy(self, board, player, move, flag):
        nboard = consts.board2ndarray(board)
        nplayer = self.players_d[player]
        spots_left = set(x for x in consts.legal if board[x] == oc.EMPTY)
        brackets = find_all_brackets(nboard, nplayer, spots_left)
        root = Node(0, nboard, nplayer, spots_left, None, brackets, -1)
        last_best = -1
        cur_best = -1
        for d in self.depthlist:
            last_best = cur_best
            temp, cur_best = AlphaBeta(root, d, -inf, inf, self.tMatrix, nplayer, flag)
            print(d, cur_best)
            if not flag.value:
                break
        move.value = last_best if last_best != -1 else cur_best
            
