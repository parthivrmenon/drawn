import sys
import os
import argparse
from drawn import Parser, Compiler


def read_file(file_path: str) -> list[str]:
    with open(file_path, "r") as f:
        return f.readlines()


def save_dot(dot_src: str, output_file: str):
    with open(output_file, "w") as f:
        f.write(dot_src)


if __name__ == "__main__":
    # Set up argument parser
    parser = argparse.ArgumentParser(
        description="Drawn - A lightweight CLI tool for diagrams-as-code"
    )
    parser.add_argument(
        "input_file", 
        help="Path to the .drawn source file"
    )
    parser.add_argument(
        "-o", "--output", 
        help="Output filename without extension (defaults to input filename stem)"
    )
    parser.add_argument(
        "-f", "--format", 
        choices=["svg", "png", "pdf"], 
        default="svg", 
        help="Output format (svg, png, or pdf)"
    )
    
    args = parser.parse_args()
    
    # Validate input file exists
    if not os.path.exists(args.input_file):
        print(f"Error: Input file '{args.input_file}' not found")
        sys.exit(1)
    
    # Determine output filename
    output_file = args.output
    if not output_file:
        # Use input filename stem as default
        output_file = os.path.splitext(os.path.basename(args.input_file))[0]
    
    # Read and parse the input file
    flows = read_file(args.input_file)
    nodes, edges = Parser(flows).parse()
    
    # Compile and render the diagram
    c = Compiler(
        nodes,
        edges,
        output_format=args.format,
        output_file=output_file,
    )
    c.compile()
    c.render()
    
    # Print output information
    print(f"Generated diagram: {output_file}.{args.format}")
