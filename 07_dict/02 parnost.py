"""
💻 parnost
za danu listu brojeva stvori rječnik u kojemu ćeš imati 
podlistu parnih i podlistu neparnih brojeva sortiranih uzlazno.
Npr. za [4, 5, 1, 3, 2] se dobije rječnik 
{'parni': [2,4], 'neparni': [1,3,5]}

💡 Moguće je riješiti u jednoj liniji.
"""    
def parnost(lista):
    rj = {"parni": [],
          "neparni": []}

    for br in sorted(lista):
        if br % 2 == 0:
            rj["parni"].append(br)
        else:
            rj["neparni"].append(br)
    return rj


def parnost(lista):
    return {"parni": [br for br in sorted(lista) if br % 2 == 0],
            "neparni": [br for br in sorted(lista) if br % 2 == 1]}


def test(fun, *args_expected):

    def pprint(*args, as_repr=True, offset=0, sep=" ", end="\n"):
        import pprint as pp
        formatted_args = []
        for arg in args:
            if as_repr:
                if isinstance(arg, (list, tuple, set, frozenset, dict)) and len(arg) > 1 and all(isinstance(row, (list, tuple, set, frozenset, dict)) for row in arg):
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
    title(parnost, "Moguće je riješiti u jednoj liniji")
    test(parnost, [4, 5, 1, 3, 2], {'parni': [2,4], 'neparni': [1,3,5]})
