import sys

from drawn import __version__
from drawn.compiler import Compiler
from drawn.config import Config
from drawn.parser import Parser
from drawn.reader import Reader


def main():
    if len(sys.argv) < 2:
        print("Usage: drawn <file_path>")
        sys.exit(1)

    if sys.argv[1] == "--version":
        # read __version__ from drawn/__init__.py
        print(f"drawn version {__version__}")
        sys.exit(0)

    file_path = sys.argv[1]
    reader = Reader(file_path)
    flows, configs = reader.flows, reader.configs

    config = Config(configs)
    nodes, edges = Parser(flows).parse()
    compiler = Compiler(nodes, edges, config=config)
    compiler.render()


if __name__ == "__main__":
    main()
