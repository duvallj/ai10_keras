import os
import numpy as np
import Othello_Core as oc
from keras.utils import to_categorical

legal = (11, 12, 13, 14, 15, 16, 17, 18, 21, 22, 23, 24, 25, 26, 27, 28, 31, 32, 33, 34, 35, 36, 37, 38, 41, 42, 43, 44, 45, 46, 47, 48, 51, 52, 53, 54, 55, 56, 57, 58, 61, 62, 63, 64, 65, 66, 67, 68, 71, 72, 73, 74, 75, 76, 77, 78, 81, 82, 83, 84, 85, 86, 87, 88)
players = {oc.BLACK: 1,
           oc.EMPTY: 0,
           oc.WHITE: -1
           }

NUM_CLASSES = 13

def score2encoding(score):
    s = abs(score)
    e = 0
    if 1<=s<=2:     e=1
    elif 3<=s<=4:   e=2
    elif 5<=s<=8:   e=3
    elif 9<=s<=16:  e=4
    elif 17<=s<=32: e=5
    elif 33<=s<=64: e=6
    
    if score < 0: e *= -1
    
    return e+6

def convert(filename):
    ifile = open(filename, 'r')
    boards = []
    scores = []
    
    for line in ifile:
        ldata = line.split(" ")
        boards.append(ldata[0])
        scores.append(ldata[1])
        
    np_boards = np.array([
        [
            players[board[spot]] for spot in legal
        ] for board in boards
    ])
    
    np_scores = to_categorical(np.array([
        [
            score2encoding(int(score))
        ] for score in scores
    ]), NUM_CLASSES)
    
    return np_boards, np_scores

def main1():
    files = [file for file in os.listdir(os.getcwd()) if file.startswith('log')]
    data = None
    labels = None
    for fname in files:
        print(fname)
        data_new, labels_new = convert(fname)
        if data is not None: data = np.concatenate((data, data_new))
        else: data = data_new
        if labels is not None: labels = np.concatenate((labels, labels_new))
        else: labels = labels_new
    print("Saving data...")
    np.savez('train_data.npz', x_train=data, y_train=labels)
    print("Done")

if __name__=='__main__':
    main1()
