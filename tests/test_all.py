import pytest
import os
import json
from drawn import Compiler, Node, Edge, Parser, Reader, Config


def test_reader():
    r = Reader("./tests/flow.drawn")
    assert len(r.flows) == 6
    assert len(r.configs) == 5



def test_default_config():
    default_config = Config()
    assert default_config.output_file == "flow"
    assert default_config.output_format == "svg"
    assert default_config.comment == "Flow"

    # Graph attributes
    assert default_config.graph_dpi == "300"
    assert default_config.graph_rankdir == "TB"
    assert default_config.graph_splines == "ortho"
    assert default_config.graph_pad == "0.2"
    assert default_config.graph_nodesep == "1"
    assert default_config.graph_ranksep == "0.8"

    # Node attributes
    assert default_config.node_margin == "0.15,0.1"
    assert default_config.node_fontname == "Courier"
    assert default_config.node_fontsize == "12"
    assert default_config.node_shape == "box"

    # Edge attributes
    assert default_config.edge_fontname == "Courier"
    assert default_config.edge_fontsize == "12"
    assert default_config.edge_arrowhead == "normal"
    assert default_config.edge_penwidth == "0.8"

    # Theme defaults
    assert default_config.theme == "light"
    assert default_config.graph_bgcolor == "white"
    assert default_config.node_color == "black"
    assert default_config.node_fontcolor == "black"
    assert default_config.node_fillcolor == "white"
    assert default_config.node_style == "filled"
    assert default_config.edge_color == "black"
    assert default_config.edge_fontcolor == "black"



def test_themes():
    dark_theme_config = Config(["% theme: dark"])
    assert dark_theme_config.graph_bgcolor == "black"
    assert dark_theme_config.node_fillcolor == "black"
    assert dark_theme_config.node_fontcolor == "white"
    assert dark_theme_config.node_color == "white"
    assert dark_theme_config.edge_color == "white"
    assert dark_theme_config.edge_fontcolor == "white"

    light_theme_config = Config(["% theme: light"])
    assert light_theme_config.graph_bgcolor == "white"
    assert light_theme_config.node_color == "black"
    assert light_theme_config.node_fillcolor == "white"
    assert light_theme_config.node_fontcolor == "black"
    assert light_theme_config.edge_color == "black"
    assert light_theme_config.edge_fontcolor == "black"

    matrix_theme_config = Config(["% theme: matrix"])
    assert matrix_theme_config.graph_bgcolor == "black"
    assert matrix_theme_config.node_fontcolor == "#00FF00"
    assert matrix_theme_config.node_fillcolor == "#001100"
    assert matrix_theme_config.node_color == "#00FF00"
    assert matrix_theme_config.edge_color == "#00FF00"
    assert matrix_theme_config.edge_fontcolor == "#00FF00"


def test_custom_config():
    custom_config = Config(
        [
            "% output_file: flow",
            "% output_format: png",
            "% comment: Flow",
            # Graph attributes
            "% graph_bgcolor: white",
            "% graph_dpi: 300",
            "% graph_rankdir: TB",
            "% graph_splines: ortho",
            "% graph_pad: 0.2",
            "% graph_nodesep: 1",
            "% graph_ranksep: 0.8",
            # Node attributes
            "% node_fontcolor: white",
            "% node_fontname: Courier",
            "% node_fontsize: 12",
            "% node_shape: box",
            "% node_style: filled",
            "% node_fillcolor: transparent",
            "% node_margin: 0.15,0.1",
            # Edge attributes
            "% edge_fontname: Courier",
            "% edge_fontsize: 12",
            "% edge_arrowhead: normal",
            "% edge_penwidth: 0.8",
            "% edge_color: white",
            "% edge_fontcolor: white",

            # Use dark theme
            "% theme: dark"
        ]
    )
    assert custom_config.output_file == "flow"
    assert custom_config.output_format == "png"
    assert custom_config.comment == "Flow"

    # Graph attributes
    assert custom_config.graph_dpi == "300"
    assert custom_config.graph_rankdir == "TB"
    assert custom_config.graph_splines == "ortho"
    assert custom_config.graph_pad == "0.2"
    assert custom_config.graph_nodesep == "1"
    assert custom_config.graph_ranksep == "0.8"

    # Node attributes
    assert custom_config.node_fontname == "Courier"
    assert custom_config.node_fontsize == "12"
    assert custom_config.node_shape == "box"
    assert custom_config.node_style == "filled"
    assert custom_config.node_margin == "0.15,0.1"

    # Edge attributes
    assert custom_config.edge_color == "white"
    assert custom_config.edge_fontcolor == "white"
    assert custom_config.edge_fontname == "Courier"
    assert custom_config.edge_fontsize == "12"
    assert custom_config.edge_arrowhead == "normal"
    assert custom_config.edge_penwidth == "0.8"

    # Colors should be applied
    assert custom_config.theme == "dark"
    assert custom_config.graph_bgcolor == "black"
    assert custom_config.node_fontcolor == "white"
    assert custom_config.node_fillcolor == "black"
    assert custom_config.node_color == "white"


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
    dot_src = Compiler(nodes, edges, Config()).compile()
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
