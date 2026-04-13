def pong(r, s, d):
    a = [[0 for _ in range(s)] for _ in range(r)]
    x = y = 0
    dx, dy = 1 if r > 1 else 0, 1 if s > 1 else 0

    for b in range(1, d + 1):
        a[x][y] = b

        if dx == 0:
            pass
        elif dx == 1:
            if 0 < x == r - 1:
                dx = -1
        else:
            if x == 0:
                dx = 1

        if dy == 0:
            pass
        elif dy == 1:
            if y == s - 1:
                dy = -1
        else:
            if y == 0:
                dy = 1

        x += dx
        y += dy

        
    return a

from helper import *

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
