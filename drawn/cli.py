import sys

from drawn import __version__
from drawn.compiler import Compiler
from drawn.reader import Reader


def main():
    if len(sys.argv) < 2:
        print("Usage: drawn <file_path>")
        sys.exit(1)

    if sys.argv[1] == "--version":
        print(f"drawn version {__version__}")
        sys.exit(0)

    file_path = sys.argv[1]
    digraph = Reader(file_path).read()
    compiler = Compiler(digraph)
    compiler.render()


if __name__ == "__main__":
    main()
