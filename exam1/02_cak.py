def cak(znakovi, koraci):
    n = len(znakovi)

    if n == 1:
        return znakovi[0] * len(koraci)

    i = 0
    rezultat = ""

    for k in koraci:
        s = 1 if k > 0 else -1
        for _ in range(abs(k)):
            if i == 0 and s == -1:
                i += 1
                s = 1
            elif i == n - 1 and s == 1:
                i -= 1
                s = -1
            else:
                i += s

        rezultat += znakovi[i]
    return rezultat

from helper import *
test(cak, "abcde", [1, 2], "bd")
test(cak, "abcdef", [1, 2, 3], "bde")
test(cak, "abcdef", [1, 2, 3, -4, 2], "bdeac")

test(cak, "abcdef", [-1], "b")        # 0 -> -1 -> odbijanje -> 1
test(cak, "abcdef", [-2], "c")        # 0 -> -2 -> odbijanje -> 2
test(cak, "abcdef", [3, -2], "db")    # 0->3='d', 3->1='b'

test(cak, "abcde", [10], "c")
test(cak, "abcde", [12], "e")
test(cak, "abcde", [200], "a")

test(cak, "a", [1, 2, 3], "aaa")
test(cak, "x", [-100, 0, 100], "xxx")
test(cak, "xywz", [1, -100, 0, 100], "yzzy")
