"""
💻 trokut
Za dane stranice trokuta a, b i c vrati njegovu površinu.
U slučaju da stranice a, b i c nisu valjanje stranice trokuta 
onda vrati None
"""
def trokut(a, b, c):
    if (isinstance(a, int) or isinstance(a, float)) and \
       (isinstance(b, int) or isinstance(b, float)) and \
       (isinstance(c, int) or isinstance(c, float)) and \
       (a + b > c) and \
       (a + c > b) and \
       (b + c > a):

       s = (a + b + c) / 2
       o = (s * (s - a) * (s - b) * (s - c)) ** 0.5
       return o
    

###############################
#        Ne dirati kod!       #
###############################
def test(func, *ulazi_ocekivano):
    """
    Jednostavna test() funkcija koja se koristi u main() za ispis
    što dana funkcija vraća, odnosno što se traži od nje.
    """
    *ulazi, ocekivano = ulazi_ocekivano
    ulazi_str = ', '.join(repr(u) for u in ulazi)
    print(f" {func.__name__}({ulazi_str}) ⮕ ",end="")
    izlazi = func(*ulazi)
    if izlazi == ocekivano:
        print(f"{izlazi!r} 👍")
    else:
        print(f"{izlazi!r} ❌ != {ocekivano!r}")

def title(func, comment=None):
    """Ispis naziva funkcije"""
    print(f"\n💻 {func.__name__}{f' (💡 {comment})' if comment else ''}")

# Standardna shema za zvanje main() funkcije.
if __name__ == '__main__':
    title(trokut)
    test(trokut, 3, 4, 5, 6)
    test(trokut, 5, 5, 5, 10.825317547305483)
    test(trokut, 3, 0, 5, None)
    test(trokut, 3, "4", 5, None)
    test(trokut, 1, 2, 3, None)


