"""
💻 suma_parnih
Za dani prirodni broj n vrati sumu svih parnih brojeva
manjih od n.
Npr. za n = 10, brojevi koji su parni i manji od 10 su
2, 4, 6, 8 i njihova suma je 20
Koristiti while petlju.
"""
def suma_parnih(n):
    s = 0
    i = 2
    while i < n:
        s += i
        i += 2        
    return s


##################################################
#           Ne dirati kod!                       #
##################################################
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

def title(fun, comment=None):
    """Ispis naziva funkcije"""
    print(f"\n💻 {fun.__name__}",end="")
    if comment:
        print(f" (💡 {comment})", end="")
    print()

def main():
    """
    main() pozivi gornjih funkcija s testnim ulazima,
    koristi test() za provjeru je li rezultat dobar ili nije
    """
    title(suma_parnih)
    test(suma_parnih, 10, 20)
    test(suma_parnih, 15, 56)
    test(suma_parnih, 100, 2450)


# Standardna shema za zvanje main() funkcije.
if __name__ == '__main__':
    main()

