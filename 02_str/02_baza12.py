"""
💻 baza12
Za dani broj u brojevnom sustavu s bazom 12 vrati vrijednost
tog broja u dekadskom brojevnom sustavu.
Npr., za broj b3a8 u bazi 12 se dobije 19568 u dekadskoj bazi
Napomena: znamenka "a" i "b" odgovaraju dekadskim brojevima 10 i 11
"""
def baza12(b12):
    b10 = 0
    p = len(b12) - 1
    for z12 in b12:
        if z12 == "a":
            z10 = 10
        elif z12 == "b":
            z10 = 11
        else:
            z10 = int(z12)

        b10 += z10 * 12 ** p
        p -= 1
    return b10


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
    title(baza12)
    test(baza12, "b3a8", 19568)
    test(baza12, "ab", 131)
    test(baza12, "13", 15)


# Standardna shema za zvanje main() funkcije.
if __name__ == '__main__':
    main()

