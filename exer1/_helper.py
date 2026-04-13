from pathlib import Path
from datetime import datetime
import sys
import inspect
import json
import uuid
import types
import py_compile
import shutil
import zipfile
import pprint as pp

class LogManager:

    def __init__(self, path=None, filename="_log.json", encoded=False):
        self.encoded = encoded
        if path is None:
            self.path = Path(__file__).parent / filename
        else:
            self.path = path

        self.data = self._load()

    @staticmethod
    def scramble(txt, key=42):
        return "".join(chr(ord(c) ^ key) for c in txt)

    @staticmethod
    def unscramble(txt, key=42):
        return "".join(chr(ord(c) ^ key) for c in txt)


    def _load(self):
        if self.path.exists():
            with open(self.path, "r", encoding="utf-8") as fp:
                if not self.encoded:
                    return json.load(fp)
                else:
                    txt = fp.read()
                    decoded = self.unscramble(txt)
                    return json.loads(decoded)
        return {}

    def has_data(self):
        return bool(self.data)

    def save(self):
        with open(self.path, "w", encoding="utf-8") as fp:
            if not self.encoded:
                json.dump(self.data, fp, ensure_ascii=False, indent=2)
            else:
                txt = json.dumps(self.data, ensure_ascii=False, indent=2)
                encoded = self.scramble(txt)
                fp.write(encoded)

    def save_decoded(self):
        with open(self.path, "w", encoding="utf-8") as fp:
                json.dump(self.data, fp, ensure_ascii=False, indent=2)

    def log_name(self, name):
        self.data["name"] = name
        self.data["id"] = uuid.getnode()

        self.save()

    def log_fun(self, fun):
        fname = fun.__name__

        if fname not in self.data:
            self.data[fname] = []

        now = datetime.now()
        time = now.strftime("%Y.%m.%d %H:%M:%S.%f")[:-3]
        src = inspect.getsource(fun)

        self.data[fname].append({
            "num": len(self.data[fname]),
            "time": time,
            "src": src
        })

        self.save()

class TestRunner:

    counter = 0

    def __init__(self, log=None):
        if not log:
            log = LogManager()
        self.log = log

    def test_counter(method):
        
        def wrapper(self, fun, *args_expected):
            if TestRunner.counter == 0:
                self.log.log_fun(fun)
            TestRunner.counter += 1
            
            # Poziv originalne metode
            return method(self, fun, *args_expected)
        
        wrapper.__name__ = method.__name__
        return wrapper        

    @staticmethod        
    def pprint(*args, as_repr=True, offset=0, sep=" ", end="\n"):
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

    @test_counter
    def ttest(self, fun, *args_expected):
        *args, expected = args_expected

        offset = self.pprint(f" {fun.__name__}(", as_repr=False, offset=0, sep="", end="")
        offset = self.pprint(*args, as_repr=True, offset=offset, sep=", ", end="")
        offset = self.pprint(") ➜ ", as_repr=False, offset=offset, sep="", end="")

        izlazi = fun(*args)

        offset = self.pprint(izlazi, as_repr=True, offset=offset, sep=", ", end="")
        if izlazi == expected:
            self.pprint(" 👍", offset=offset, as_repr=False, end="")
        else:
            offset = self.pprint(" ❌ != ", as_repr=False, offset=offset, end="")
            self.pprint(expected, as_repr=True, offset=offset, end="")
        print()
        print()    

    @test_counter
    def test(self, fun, *args_expected):
        *args, expected = args_expected
        args_str = ", ".join(repr(a) for a in args)
        result = fun(*args)

        print(f"{fun.__name__}({args_str}) ➜ ", end="")
        if result == expected:
            print(f"{result!r} 👍")
        else:
            print(f"{result!r} ❌ != {expected!r}")

    def title(self, fun):
        print(fun.__name__)

class UserInterface:

    @classmethod
    def prompt(cls, input_fun):
        rawname = None
        while not rawname:
            rawname = input_fun()
            if rawname:
                words = rawname.strip().split()
                if len(words) >= 2:
                    name = " ".join(words).title()
                    return name
                else:
                    rawname = None

    @classmethod
    def ask_name(cls):
        try:
            import tkinter as tk
            from tkinter import simpledialog
            root = tk.Tk()
            root.withdraw()
            name = cls.prompt(lambda: simpledialog.askstring("🧑‍🏫", "Unesi ime i prezime: "))
            root.destroy()
        except:
            name = cls.prompt(lambda: input("🧑‍🏫 Unesi ime i prezime: "))
        return name

class ExecutionTracer:

    def __init__(self):
        self._clean()

    def _clean(self):
        self.calls = []
        self.misc = []

    def _profile_hook(self, frame, event, arg):
        """Internal hook method to process execution events."""
        if event == 'c_call':
            self.misc.append(arg)
            self.calls.append(arg)

            func_name = arg.__name__

            arg_instance = getattr(arg, "__self__", None)
            if arg_instance is None:
                # it is func call
                module_name = getattr(arg, '__module__', 'builtins')
                self.calls.append(f"FUN {module_name}.{func_name}")
            else:
                # it is method call

                class_name = arg_instance.__class__.__name__
                module_name = arg_instance.__class__.__module__
                if isinstance(arg_instance.__class__, types.ModuleType):
                    self.calls.append(f"FUN {module_name}.{func_name}")
                else:
                    module_name = arg_instance.__class__.__module__
                    self.calls.append(f"MTDx {module_name}.{class_name}.{func_name}")

        elif event == 'call':
            self.misc.append(frame.f_code)
            func_name = frame.f_code.co_name

            # print("----", func_name)
            arg_instance = frame.f_locals.get('self')

            if arg_instance is None:
                arg_instance = frame.f_locals.get('cls')

            if arg_instance is None:
                module_name = frame.f_globals.get('__name__', 'unknown')
                self.calls.append(f"aFUN {module_name}.{func_name}")

            elif isinstance(arg_instance, types.ModuleType):
                # --- CASE B: It's a function inside a module (rare for 'call') ---
                module_name = arg_instance.__name__
                self.calls.append(f"bFUN {module_name}.{func_name}")
            else:
                class_name = arg_instance.__class__.__name__
                module_name = arg_instance.__class__.__module__
                self.calls.append(f"cMTD {module_name}.{class_name}.{func_name}")


    def __enter__(self):
        """Starts the tracing."""
        sys.setprofile(self._profile_hook)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Stops the tracing automatically."""
        sys.setprofile(None)
        # remove last 2 calls (__exit__, setprofile)
        self.calls = self.calls[:-2]

    def trace(self, fun, *args, **kwargs):
        """Convienence method to trace a specific function call."""
        with self:
            return fun(*args, **kwargs)

class Installer:

    @staticmethod
    def pack(zipname="help.zip"):
        filenames = [f.name for f in Path(__file__).parent.glob("*") if f.suffix in (".py", ".json")]
        with zipfile.ZipFile(zipname, "w") as new_zip:
            for filename in filenames:
                new_zip.write(filename)
    
    @staticmethod
    def unpack(zipname):
        pass

    @staticmethod
    def compile():
        py_file = Path(__file__)

        if py_file.suffix == ".py":
            pyc_file = py_file.parent / f"{py_file.stem}.pyc"
            py_compile.compile(py_file, cfile=pyc_file)
            
            pyc_folder = py_file.parent / "__pycache__"
            if pyc_folder.exists() and pyc_folder.is_dir():
                shutil.rmtree(pyc_folder)

            py_file.unlink()        



def main(log=None, forced=False):
    if log is None:
        log = LogManager()
    if not log.has_data() or forced:
        name = UserInterface.ask_name()
        log.log_name(name)


if len(sys.argv) > 1:
    arg1 = sys.argv[1].lower()
    if arg1 == "help":
        print("compile : make helper.pyc from helper.py and delede .py file")
        print("zip name.zip : zip all .py files")
        print("")

    if arg1 == "compile":
        Installer.compile()

    elif arg1 == "zip":
        Installer.pack()
else:
    ENCODED = False

    log = LogManager(encoded=ENCODED)
    main(log)
    runner = TestRunner(log)
    test = runner.ttest
    title = runner.title




