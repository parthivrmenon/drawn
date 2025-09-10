import sys
from drawn import Parser, Compiler, Reader, Config

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python main.py <file_path>")
        sys.exit(1)

    # Read and parse the input file
    reader = Reader(sys.argv[1])
    flows = reader.flows
    configs = Config(reader.configs)
    nodes, edges = Parser(flows).parse()

    # Compile and render the diagram
    c = Compiler(nodes, edges, config=configs)
    c.render()
