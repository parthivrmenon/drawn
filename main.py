import sys
from drawn import Parser, Compiler


def read_file(file_path: str) -> list[str]:
    with open(file_path, "r") as f:
        return f.readlines()


def save_dot(dot_src: str, output_file: str):
    with open(output_file, "w") as f:
        f.write(dot_src)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python main.py <file_path>")
        sys.exit(1)
    flows = read_file(sys.argv[1])
    nodes, edges = Parser(flows).parse()
    c = Compiler(
        nodes,
        edges,
        output_format="svg",
        comment="Flow",
        output_file="drawn_flow",
    )
    c.compile()
    c.render()
