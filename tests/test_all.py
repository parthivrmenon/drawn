import pytest
import os
import json
from drawn import Compiler, Node, Edge, Parser


def test_parser():
    nodes, edges = Parser(
        flows=[
            "Sun --> Evaporation",
            "Evaporation -(condensation)-> Clouds",
            "Clouds -(precipitation)-> Rain",
            "Rain --> Oceans",
            "Oceans -(evaporation)-> Clouds",
        ]
    ).parse()
    assert len(nodes) == 5
    assert len(edges) == 5


def test_compiler():
    nodes = [
        Node("Sun", "Sun"),
        Node("Evaporation", "Evaporation"),
        Node("Clouds", "Clouds"),
        Node("Rain", "Rain"),
        Node("Oceans", "Oceans"),
    ]
    edges = [
        Edge(nodes[0], nodes[1]),
        Edge(nodes[1], nodes[2], "condensation"),
        Edge(nodes[2], nodes[3], "precipitation"),
        Edge(nodes[3], nodes[4]),
        Edge(nodes[4], nodes[2], "evaporation"),
    ]
    dot_src = Compiler(nodes, edges).compile()
    assert type(dot_src) == str
    lines = dot_src.splitlines()
    assert "// Flow" in lines[0]
    assert "digraph" in lines[1]
    assert "\tSun [label=Sun]" in lines
    assert "\tEvaporation [label=Evaporation]"
    assert "\tClouds [label=Clouds]" in lines
    assert "\tOceans [label=Oceans]" in lines
    assert "\tSun -> Evaporation" in lines
    assert "\tEvaporation -> Clouds [xlabel=condensation]" in lines
    assert "\tClouds -> Rain [xlabel=precipitation]" in lines
    assert "\tRain -> Oceans" in lines
    assert "\tOceans -> Clouds [xlabel=evaporation]" in lines


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
