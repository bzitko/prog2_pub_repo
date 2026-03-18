"""
💻 potencije
Za dani prirodni broj n vrati uzlaznu listu 
svih potencija broja 2.
"""
def potencije(n):
    lista = []
    i = 0
    while 2 ** i < n:
        lista.append(2**i)
        i += 1
    return lista

def potencije(n):
    lista = []
    p = 1
    while p < n:
        lista.append(p)
        p *= 2
    return lista    

# ======================================================
# ⚙️  TESTNI OKVIR – NE MIJENJAJTE KOD ISPOD!
# Ovaj dio automatski provjerava ispravnost rješenja.
# ======================================================
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
    title(potencije)
    test(potencije, 1, [])
    test(potencije, 2, [1])
    test(potencije, 10, [1, 2, 4, 8])
    test(potencije, 100, [1, 2, 4, 8, 16, 32, 64])

