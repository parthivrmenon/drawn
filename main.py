
import sys
from drawn.parser import parse, read_file
from drawn.render import render_graphviz


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python main.py <file_path>")
        sys.exit(1)

    flows = read_file(sys.argv[1])
    edges = parse(flows)
    render_graphviz(edges, "drawn_flow", "svg")



    


    