def okvir(n):
    m = []

    for i in range(n):
        red = []
        for j in range(n):
            top = i
            left = j
            bottom = n - 1 - i
            right = n - 1 - j

            val = min(top, left, bottom, right) + 1
            red.append(val)
        m.append(red)
    return m

from helper import *
test(okvir, 1, [[1]])
test(okvir, 2, [[1, 1], 
                [1, 1]])
test(okvir, 3, [[1, 1, 1], 
                [1, 2, 1], 
                [1, 1, 1]])
test(okvir, 4, [[1, 1, 1, 1], 
                [1, 2, 2, 1], 
                [1, 2, 2, 1], 
                [1, 1, 1, 1]])
test(okvir, 5, [[1, 1, 1, 1, 1], 
                [1, 2, 2, 2, 1], 
                [1, 2, 3, 2, 1], 
                [1, 2, 2, 2, 1], 
                [1, 1, 1, 1, 1]])