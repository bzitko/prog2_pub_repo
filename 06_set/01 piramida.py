"""
💻 piramida
za zadanu listu skupova, sukcesivno gradi piramidu radeći presjek 
susjednih skupova dok ne preostane samo jedan (vršni) skup.

Primjer: za [{1, 2, 3}, {2, 3, 4}, {3, 4, 5}]
prvo se dobije      [{2, 3}, {3, 4}]
zatim                    [{3}]
i vraća se                {3}
"""    
def piramida(lista_skupova):
    if not lista_skupova:
        return set()
    
    red = lista_skupova
    
    # Ponavljaj proces dok ne ostane samo jedan skup u redu
    while len(red) > 1:
        novi_red = []
        for i in range(len(red) - 1):
            # Radi presjek susjednih skupova u piramidi
            presjek = red[i] & red[i+1]
            novi_red.append(presjek)
        red = novi_red
        
    return red[0] if red else set()


def test(fun, *args_expected):

    def pprint(*args, as_repr=True, offset=0, sep=" ", end="\n"):
        import pprint as pp
        formatted_args = []
        for arg in args:
            if as_repr:
                if isinstance(arg, (list, tuple)) and len(arg) > 1 and all(isinstance(row, (list, tuple)) for row in arg):
                    width = max(len(repr(row)) for row in arg) + 2
                    lines = pp.pformat(arg, width=width, sort_dicts=False).split("\n")
                    lines = [line.ljust(width, " ") for line in lines]
                    formatted_args.append(lines)
                elif isinstance(arg, dict) and len(arg) > 1:
                    width = max(len(repr(item)) for item in arg.items())
                    lines = pp.pformat(arg, width=width, sort_dicts=False).split("\n")
                    lines = [line.ljust(width, " ") for line in lines]
                    formatted_args.append(lines)
                else:
                    formatted_args.append(repr(arg))
            else:
                formatted_args.append(str(arg))

        # Ispis argumenata
        pos = 0
        for i, arg in enumerate(formatted_args):
            if isinstance(arg, str):
                print(arg, end="")
                pos += len(arg)
            else:
                print(arg[0])
                if offset:
                    pos += offset
                    offset = 0
                for line in arg[1:-1]:
                    print(" " * pos + line)
                print(" " * pos + arg[-1], end="")
                pos += len(arg[-1])

            if i < len(formatted_args) - 1:
                print(sep, end="")
                pos += len(sep)

        pos += offset
        pos += len(str(end))
        print(end=end)
        return pos    
    
    *args, expected = args_expected

    offset = pprint(f" {fun.__name__}(", as_repr=False, offset=0, sep="", end="")
    offset = pprint(*args, as_repr=True, offset=offset, sep=", ", end="")
    offset = pprint(") ⮕ ", as_repr=False, offset=offset, sep="", end="")

    izlazi = fun(*args)

    offset = pprint(izlazi, as_repr=True, offset=offset, sep=", ", end="")
    if izlazi == expected:
        pprint(" 👍", offset=offset, as_repr=False, end="")
    else:
        offset = pprint(" ❌ != ", as_repr=False, offset=offset, end="")
        pprint(expected, as_repr=True, offset=offset, end="")
    print()
    print()    

def title(func, comment=None):

    print(f"\n💻 {func.__name__}{f' (💡 {comment})' if comment else ''}")

if __name__ == '__main__':
    title(piramida)
    test(piramida, [{1, 2, 3}, {2, 3, 4}, {3, 4, 5}], {3})
    test(piramida, [{1, 2}, {2, 3}, {4, 5}], set())
    test(piramida, [{"a", "b", "c"}, {"b", "c", "d"}, {"c", "d", "e"}, {"d", "e", "f"}], set())
    test(piramida, [{1, 2}, {1, 2, 3}, {1, 3}, {1, 4}], {1})
    test(piramida, [{1, 2, 3, 4, 5, 6},
                    {2, 3, 4, 5, 6, 7},
                    {3, 4, 5, 6, 7, 8},
                    {4, 5, 6, 7, 8, 9},
                    {5, 6, 7, 8, 9, 10}], {5, 6})

