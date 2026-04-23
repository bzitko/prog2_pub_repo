"""
💻 prevedi
uz pomoć zadanog rječnika prijevoda s hrvatskog na engleski jezik, 
prevedi čestitku s hrvatskog jezika na engleski jezik.

Npr. za rječnik
{'sretan': 'happy',
 'sretna': 'happy',
 'nova': 'new',
 'godina': 'year',
 'čestit': 'merry',
 'božić': 'christmas',
 'i': 'and'}

i čestitku 

"Čestit Božić i sretna Nova godina"

dobije se

"merry christmas and happy new year"

💡 Moguće je riješiti u jednoj liniji.
"""    
def prevedi(rjecnik, cestitka_hr):
    rijeci_hr = cestitka_hr.lower().split()
    rijeci_en = [rjecnik[rijec_hr] for rijec_hr in rijeci_hr]
    return " ".join(rijeci_en)

def prevedi(rjecnik, cestitka_hr):
    return " ".join([rjecnik[rijec_hr] for rijec_hr in cestitka_hr.lower().split()])


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
    title(prevedi, "Moguće je riješiti u jednoj liniji")
    test(prevedi, {'sretan': 'happy',
                   'sretna': 'happy',
                   'nova': 'new',
                   'godina': 'year',
                   'čestit': 'merry',
                   'božić': 'christmas',
                   'i': 'and'},         "Čestit Božić i sretna Nova godina", "merry christmas and happy new year")
