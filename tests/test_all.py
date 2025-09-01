import pytest 
import os

from drawn.parser import parse, read_file
from drawn.render import render_graphviz  

def test_read_file():
    flows = read_file("flow.drawn")
    assert len(flows) == 3

def test_parser():
    flows = [
        "API --> Server --> DB",
        "Server --> Cache",
        "Server --> Logger"
    ]
    edges = parse(flows)
    assert len(edges) == 4
    assert edges[0] == ("API", "Server")
    assert edges[1] == ("Server", "DB")
    assert edges[2] == ("Server", "Cache")
    assert edges[3] == ("Server", "Logger")

def test_render():
    flows = [
        "API --> Server --> DB",
        "Server --> Cache",
        "Server --> Logger"
    ]
    edges = parse(flows)
    render_graphviz(edges, "drawn_flow", "png")
    assert os.path.exists("drawn_flow.png")

#     # cleanup
#     #os.remove("drawn_flow.png")



