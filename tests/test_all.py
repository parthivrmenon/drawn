import pytest
import os
import json
from drawn import Compiler, Node, Edge, Parser


def test_parser():
    nodes, edges = Parser(
        flows=[
            "API -(auth)-> Server --> DB --> Logger",
            "Server -(hit)-> Cache",
            "Server --> Logger",
        ]
    ).parse()
    assert len(nodes) == 5
    assert len(edges) == 5


def test_compiler():
    nodes = [
        Node("API", "API"),
        Node("Server", "Server"),
        Node("DB", "DB"),
    ]
    edges = [
        Edge(nodes[0], nodes[1], "auth"),
        Edge(nodes[1], nodes[2], None),
    ]
    dot_src = Compiler(nodes, edges).compile()
    assert type(dot_src) == str
    lines = dot_src.splitlines()
    assert "// Flow" in lines[0]
    assert "digraph" in lines[1]
    assert "API [label=API]" in lines[2]
    assert "Server [label=Server]" in lines[3]
    assert "DB [label=DB]" in lines[4]
    assert "API -> Server [label=auth]" in lines[5]
    assert "Server -> DB" in lines[6]


# from drawn.parser import parse, read_file
# from drawn.render import render_graphviz

# def test_read_file():
#     flows = read_file("flow.drawn")
#     assert len(flows) == 3

# def test_parser():
#     flows = [
#         "API -(auth)-> Server --> DB --> Logger",
#         "Server -(hit)-> Cache",
#         "Server --> Logger"
#     ]
#     edges = parse(flows)
#     assert len(edges) == 5
#     assert edges[0] == ("API", "Server","auth")
#     assert edges[1] == ("Server", "DB", None)
#     assert edges[2] == ("DB", "Logger", None)
#     assert edges[3] == ("Server", "Cache", "hit")
#     assert edges[4] == ("Server", "Logger", None)


# def test_render():
#     flows = [
#         "API --> Server --> DB",
#         "Server --> Cache",
#         "Server --> Logger"
#     ]
#     edges = parse(flows)
#     render_graphviz(edges, "drawn_flow", "png")
#     assert os.path.exists("drawn_flow.png")

#     # cleanup
#     #os.remove("drawn_flow.png")
