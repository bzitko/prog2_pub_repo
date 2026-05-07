"""
💻 putovi
u matrici veličine m x n se kreće iz donjeg desnog kuta (m, n)
i želi se doći do gornjeg lijevog kuta (1, 1). Može se kretati samo 
jedno polje lijevo ili jedno polje gore.
Potrebno je izračunati koliko ukupno različitih putova postoji do cilja.
"""
def putovi(m, n):
    if (m == 0 or n == 0):
        return 1

    return putovi(m - 1, n) + putovi(m, n - 1)


def test(func, *ulazi_ocekivano):
    """
    Jednostavna test() funkcija koja se koristi u main() za ispis
    što dana funkcija vraća, odnosno što se traži od nje.
    """
    *ulazi, ocekivano = ulazi_ocekivano
    ulazi_str = ', '.join(repr(u) for u in ulazi)
    izlazi = func(*ulazi)
    print(f" {func.__name__}({ulazi_str}) ⮕ ",end="")
    if izlazi == ocekivano:
        print(f"{izlazi!r} 👍")
    else:
        print(f"{izlazi!r} ❌ != {ocekivano!r}")

def title(func, comment=None):
    print(f"\n💻 {func.__name__}{f' (💡 {comment})' if comment else ''}")

if __name__ == '__main__':
    title(putovi)
    test(putovi, 1, 1, 2)
    test(putovi, 2, 2, 6)
    test(putovi, 3, 3, 20)
    test(putovi, 9, 6, 5005)
    test(putovi, 100, 100, 20)
