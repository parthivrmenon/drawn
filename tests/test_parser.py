from drawn.model.digraph import Edge, Node
from drawn.parser import Parser


def test_parser_basic():
    """Test basic parsing with string content."""
    content = """
    Sun --> Evaporation
    Evaporation -(condensation)-> Clouds
    Clouds -(precipitation)-> Rain
    Rain --> Rivers
    Rivers --> Oceans
    Oceans -(evaporation)-> Evaporation
    """
    
    expected_nodes = ["Sun", "Evaporation", "Clouds", "Rain", "Rivers", "Oceans"]
    expected_edges = [
        ("Sun", "Evaporation", None),
        ("Evaporation", "Clouds", "condensation"),
        ("Clouds", "Rain", "precipitation"),
        ("Rain", "Rivers", None),
        ("Rivers", "Oceans", None),
        ("Oceans", "Evaporation", "evaporation"),
    ]
    
    digraph = Parser.parse(content)
    nodes = digraph.nodes
    edges = digraph.edges
    
    assert len(nodes) == 6
    assert len(edges) == 6

    for n in expected_nodes:
        assert Node(n, n) in nodes

    for e in expected_edges:
        assert (
            Edge(Node(e[0], e[0]), Node(e[1], e[1]), e[2])
            in edges
        )


def test_parser_with_config():
    """Test parsing with configuration directives."""
    content = """
    % theme: dark
    % output_file: test_diagram
    % auto_shapes: false
    
    A --> B --> C
    """
    
    digraph = Parser.parse(content)
    
    assert digraph.config.theme == "dark"
    assert digraph.config.output_file == "test_diagram"
    assert digraph.config.auto_shapes == False
    assert len(digraph.nodes) == 3
    assert len(digraph.edges) == 2


def test_parser_empty_content():
    """Test parsing empty content."""
    content = ""
    
    digraph = Parser.parse(content)
    
    assert len(digraph.nodes) == 0
    assert len(digraph.edges) == 0
    assert digraph.config.theme == "light"  # Default values
