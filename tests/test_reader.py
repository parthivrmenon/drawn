from drawn.model.digraph import Edge, Node
from drawn.reader import Reader


def test_reader():
    reader = Reader("tests/flow.drawn")
    expected_nodes = ["Sun", "Evaporation", "Clouds", "Rain", "Rivers", "Oceans"]
    expected_edges = [
        ("Sun", "Evaporation", None),
        ("Evaporation", "Clouds", "condensation"),
        ("Clouds", "Rain", "precipitation"),
        ("Rain", "Rivers", None),
        ("Rivers", "Oceans", None),
        ("Oceans", "Evaporation", "evaporation"),
    ]
    digraph = reader.read()
    nodes = digraph.nodes
    edges = digraph.edges
    assert len(nodes) == 6
    assert len(edges) == 6

    for n in expected_nodes:
        assert Node(n, n, shape="box") in nodes

    for e in expected_edges:
        assert (
            Edge(Node(e[0], e[0], shape="box"), Node(e[1], e[1], shape="box"), e[2])
            in edges
        )
