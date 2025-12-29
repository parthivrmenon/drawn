from drawn.compiler import Compiler
from drawn.model.digraph import Config, DirectedGraph, Edge, Node


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
    config = Config(
        comment="Flow",
        output_file="flow",
        output_format="svg",
        theme="light",
        auto_shapes=True,
    )
    digraph = DirectedGraph(nodes=nodes, edges=edges, config=config)
    dot_src = Compiler.compile(digraph)
    assert type(dot_src) == str
    lines = dot_src.splitlines()
    assert "// Flow" in lines[0]
    assert "digraph" in lines[1]
    assert "\tSun [label=Sun shape=box]" in lines
    assert "\tEvaporation [label=Evaporation shape=box]" in lines
    assert "\tClouds [label=Clouds shape=box]" in lines
    assert "\tOceans [label=Oceans shape=box]" in lines
    assert "\tSun -> Evaporation" in lines
    assert "\tEvaporation -> Clouds [xlabel=condensation]" in lines
    assert "\tClouds -> Rain [xlabel=precipitation]" in lines
    assert "\tRain -> Oceans" in lines
    assert "\tOceans -> Clouds [xlabel=evaporation]" in lines
