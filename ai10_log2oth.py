import os
import numpy as np
import Othello_Core as oc

legal = [11, 12, 13, 14, 15, 16, 17, 18, 21, 22, 23, 24, 25, 26, 27, 28, 31, 32, 33, 34, 35, 36, 37, 38, 41, 42, 43, 44, 45, 46, 47, 48, 51, 52, 53, 54, 55, 56, 57, 58, 61, 62, 63, 64, 65, 66, 67, 68, 71, 72, 73, 74, 75, 76, 77, 78, 81, 82, 83, 84, 85, 86, 87, 88]
players = {oc.BLACK: 1,
           oc.EMPTY: 0,
           oc.WHITE: -1
           }

def convert(filename, eval_data):
    ifile = open(filename, 'r')
    if eval_data:
        new_filename = 'test_batch.oth'
        ofile = open(new_filename, 'ab')
    else:
        new_filename = filename[:filename.index('.')] + '4' + '.oth'
        ofile = open(new_filename, 'wb')
    for line in ifile:
        ldata = line.split(' ')
        board = np.array([players[ldata[0][spot]] for spot in legal], dtype=np.uint8)
        score = np.cast[np.uint8](int(ldata[1]))
        ofile.write(bytes([score]))
        ofile.write(bytes(board))
    ifile.close()
    ofile.close()

def main1():
    files = [file for file in os.listdir(os.getcwd()) if file.endswith('log')]
    for fname in files:
        print(fname)
        convert(fname, False)

if __name__=='__main__':
    main1()
