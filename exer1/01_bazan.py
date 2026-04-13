def bazan(b, n):
    b10 = 0
    p = len(b) - 1
    for z in b.lower():
        if z.isalpha():
            z10 = 10 + ord(z) - ord("a")
        else:
            z10 = int(z)

        b10 += z10 * n ** p
        p -= 1
    return b10

from _helper import *

test(bazan, "b3a8", 12, 19568)
test(bazan, "ff", 16, 255)
test(bazan, "1001", 2, 9)
    

