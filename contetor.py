from pathlib import Path
import re
current_dir = Path.cwd()


def collect(filename):
    pattern = r'"(#+)\s+(\d+(?:\.\d+)*\.?)\s+([^"\\]*)'
    with open(filename) as fp:
        items = re.findall(pattern, fp.read())
    return items


def print_by_file(dir):
    for d in sorted(dir.iterdir()):
        if not d.is_dir() or d.name.startswith("."):
            continue
        for f in d.glob("*.ipynb"):
            print(f.name)
            for mark, num, txt in collect(f):
                print(" "*len(mark) + num + " " + txt)

def print_by_topic(dir):
    topics = {}
    for d in sorted(dir.iterdir()):
        if not d.is_dir() or d.name.startswith("."):
            continue
        for f in d.glob("*.ipynb"):
            for mark, num, txt in collect(f):
                tupnum = tuple(int(n) for n in num.rstrip(".").split("."))
                topics[tupnum] = (mark, num, txt)

    for tupnum in sorted(topics):
        mark, num, txt = topics[tupnum]
        print(" "*len(mark) + num + " " + txt)



    

print_by_topic(current_dir)

            
