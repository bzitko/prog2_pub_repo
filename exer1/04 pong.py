def pong(r, s, d):
    a = [[0 for _ in range(s)] for _ in range(r)]
    i = j = 0
    di, dj = 1 if r > 1 else 0, 1 if s > 1 else 0

    for b in range(1, d + 1):
        a[i][j] = b

        if di == 0:
            pass
        elif di == 1:
            if 0 < i == r - 1:
                di = -1
        else:
            if i == 0:
                di = 1

        if dj == 0:
            pass
        elif dj == 1:
            if j == s - 1:
                dj = -1
        else:
            if j == 0:
                dj = 1

        i += di
        j += dj

        
    return a

from _helper import *

test(pong, 1, 1, 5, [[5]])
test(pong, 1, 2, 5, [[5, 4]])
test(pong, 2, 1, 5, [[5],
                     [4]])
test(pong, 2, 2, 5, [[5, 0],
                     [0, 4]])
test(pong, 2, 3, 5, [[5, 0, 3],
                     [0, 4, 0]])
test(pong, 4, 5, 7, [[1, 0, 7, 0, 0],
                     [0, 2, 0, 6, 0],
                     [0, 0, 3, 0, 5],
                     [0, 0, 0, 4, 0]])
test(pong, 4, 5, 10, [[1, 0, 7, 0, 0], 
                      [0, 8, 0, 6, 0], 
                      [9, 0, 3, 0, 5], 
                      [0, 10, 0, 4, 0]])
test(pong, 9, 6, 15, [[ 1,  0,  0,  0,  0, 0], 
                      [ 0,  2,  0,  0,  0, 0], 
                      [ 0,  0,  3,  0, 15, 0],
                      [ 0,  0,  0, 14,  0, 0],
                      [ 0,  0, 13,  0,  5, 0],
                      [ 0, 12,  0,  0,  0, 6],
                      [11,  0,  0,  0,  7, 0],
                      [ 0, 10,  0,  8,  0, 0],
                      [ 0,  0,  9,  0,  0, 0]])
