"""
💻 flat
za danu listu koji može sadržavati druge ugniježđene liste, 
vrati spljoštenu listu svih elemenata koristeći rekurziju.
npr. za [1, [2, 3], [4, [5, 6]]] dobiva se [1, 2, 3, 4, 5, 6]
"""
def flat(lista):
    print(lista)
    if len(lista) == 0:
        return []
    
    prvi, *ostatak = lista

    if isinstance(prvi, list):
        return flat(prvi) + flat(ostatak)
    else:
        return [prvi] + flat(ostatak)

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
    title(flat)
    test(flat, [1, [2, 3], [4, [5, 6]]], [1, 2, 3, 4, 5, 6])
    test(flat, [[[[[1]]]]], [1])
    test(flat, [1, 2, 3], [1, 2, 3])
    test(flat, [[1, [2, 3]], [4, [5, [[[[[6]]]]]]]], [1, 2, 3, 4, 5, 6])
