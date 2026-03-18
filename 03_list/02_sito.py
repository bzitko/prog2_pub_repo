"""
💻 sito
Za dani prirodni broj n vrati uzlaznu listu 
svih prostih brojeva do n 
po principu erastotenovog sita

npr. za n = 10 imamo listu kandidata [2, 3, 4, 5, 6, 7, 8, 9, 10]
prvi element liste je prosti broj 2
iz liste izbacimo višekratnike od 2 pa dobijemo [3, 5, 7, 9]
prvi element liste je prosti broj 3
iz liste izbacimo višekratnike od 3 pa dobijemo [5, 7]
...
postupak ponavljamo dok ne izbacimo sve kandidate

"""
def sito(n):
    brojevi = list(range(2, n + 1))
    prosti = []
    while brojevi:
        p = brojevi[0]
        prosti.append(p)
        brojevi = [broj for broj in brojevi if broj % p != 0]
    return prosti


def test(func, *ulazi_ocekivano):
    *ulazi, ocekivano = ulazi_ocekivano
    izlazi = func(*ulazi)
    print(f"{func.__name__}({', '.join(map(repr, ulazi))}) ⮕ {izlazi!r} "
          f"{'👍' if izlazi == ocekivano else f'❌ != {ocekivano!r}'}")

def title(func, comment=None):
    """Ispis naziva funkcije"""
    print(f"\n💻 {func.__name__}{f' (💡 {comment})' if comment else ''}")

# Standardna shema za zvanje main() funkcije.
if __name__ == '__main__':
    title(sito)
    test(sito, 1, [])
    test(sito, 3, [2, 3])
    test(sito, 10, [2, 3, 5, 7])
    test(sito, 50, [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47])