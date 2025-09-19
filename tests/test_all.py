import json
import os

import pytest

from drawn.compiler import Compiler
from drawn.config import Config
from drawn.models import Edge, Node
from drawn.parser import Parser
from drawn.reader import Reader
from drawn.shapes import get_auto_shape_for_node


def test_reader():
    r = Reader("./tests/flow.drawn")
    assert len(r.flows) == 6
    assert len(r.configs) == 4


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
            "% theme: dark",
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
    print(dot_src)
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


def test_get_auto_shape_for_node():
    # Databases
    assert get_auto_shape_for_node("db") == "cylinder"
    assert get_auto_shape_for_node("DB") == "cylinder"
    assert get_auto_shape_for_node("database") == "cylinder"
    assert get_auto_shape_for_node("DATABASE") == "cylinder"
    assert get_auto_shape_for_node("sql") == "cylinder"
    assert get_auto_shape_for_node("SQL") == "cylinder"
    assert get_auto_shape_for_node("postgres") == "cylinder"
    assert get_auto_shape_for_node("POSTGRES") == "cylinder"
    assert get_auto_shape_for_node("mysql") == "cylinder"
    assert get_auto_shape_for_node("MYSQL") == "cylinder"
    assert get_auto_shape_for_node("datalake") == "cylinder"
    assert get_auto_shape_for_node("DATALAKE") == "cylinder"
    assert get_auto_shape_for_node("datawarehouse") == "cylinder"
    assert get_auto_shape_for_node("DATAWAREHOUSE") == "cylinder"

    # Caches
    assert get_auto_shape_for_node("cache") == "box3d"
    assert get_auto_shape_for_node("CACHE") == "box3d"
    assert get_auto_shape_for_node("redis") == "box3d"
    assert get_auto_shape_for_node("REDIS") == "box3d"
    assert get_auto_shape_for_node("memcached") == "box3d"
    assert get_auto_shape_for_node("MEMCACHED") == "box3d"
    assert get_auto_shape_for_node("memcached") == "box3d"
    assert get_auto_shape_for_node("MEMCACHED") == "box3d"

    # Queues
    assert get_auto_shape_for_node("queue") == "parallelogram"
    assert get_auto_shape_for_node("QUEUE") == "parallelogram"
    assert get_auto_shape_for_node("kafka") == "parallelogram"
    assert get_auto_shape_for_node("KAFKA") == "parallelogram"
    assert get_auto_shape_for_node("rabbitmq") == "parallelogram"
    assert get_auto_shape_for_node("RABBITMQ") == "parallelogram"

    # Storage
    assert get_auto_shape_for_node("storage") == "folder"
    assert get_auto_shape_for_node("STORAGE") == "folder"
    assert get_auto_shape_for_node("bucket") == "folder"
    assert get_auto_shape_for_node("BUCKET") == "folder"
    assert get_auto_shape_for_node("s3") == "folder"
    assert get_auto_shape_for_node("S3") == "folder"

    # Components
    assert get_auto_shape_for_node("api") == "component"
    assert get_auto_shape_for_node("API") == "component"
    assert get_auto_shape_for_node("server") == "component"
    assert get_auto_shape_for_node("SERVER") == "component"
    assert get_auto_shape_for_node("service") == "component"
    assert get_auto_shape_for_node("SERVICE") == "component"

    # Users
    assert get_auto_shape_for_node("user") == "ellipse"
    assert get_auto_shape_for_node("USER") == "ellipse"
    assert get_auto_shape_for_node("customer") == "ellipse"
    assert get_auto_shape_for_node("CUSTOMER") == "ellipse"


def test_auto_shapes_config():
    # Test auto_shapes enabled (default)
    config_enabled = Config()
    assert config_enabled.auto_shapes == True

    # Test auto_shapes disabled via config
    config_disabled = Config(["% auto_shapes: false"])
    assert config_disabled.auto_shapes == False

    # Test various ways to disable
    config_no = Config(["% auto_shapes: no"])
    assert config_no.auto_shapes == False

    config_off = Config(["% auto_shapes: off"])
    assert config_off.auto_shapes == False

    config_0 = Config(["% auto_shapes: 0"])
    assert config_0.auto_shapes == False

    # Test various ways to enable
    config_true = Config(["% auto_shapes: true"])
    assert config_true.auto_shapes == True

    config_yes = Config(["% auto_shapes: yes"])
    assert config_yes.auto_shapes == True

    config_1 = Config(["% auto_shapes: 1"])
    assert config_1.auto_shapes == True

    config_on = Config(["% auto_shapes: on"])
    assert config_on.auto_shapes == True


def test_compiler_auto_shapes_disabled():
    # Test that when auto_shapes is disabled, nodes don't get shape attributes
    nodes = [
        Node("UserDB", "UserDB"),
        Node("APIServer", "APIServer"),
        Node("RedisCache", "RedisCache"),
    ]
    edges = []

    config = Config(["% auto_shapes: false"])
    dot_src = Compiler(nodes, edges, config).compile()
    lines = dot_src.splitlines()

    # Should not have shape attributes when auto_shapes is disabled
    assert "\tUserDB [label=UserDB]" in lines
    assert "\tAPIServer [label=APIServer]" in lines
    assert "\tRedisCache [label=RedisCache]" in lines

    # Verify no shape attributes are present
    for line in lines:
        if "label=" in line and "[" in line:
            assert "shape=" not in line


def test_compiler_auto_shapes_enabled():
    # Test that when auto_shapes is enabled, nodes get appropriate shapes
    nodes = [
        Node("UserDB", "UserDB"),
        Node("APIServer", "APIServer"),
        Node("RedisCache", "RedisCache"),
    ]
    edges = []

    config = Config(["% auto_shapes: true"])
    dot_src = Compiler(nodes, edges, config).compile()
    lines = dot_src.splitlines()

    # Should have shape attributes when auto_shapes is enabled
    assert "\tUserDB [label=UserDB shape=cylinder]" in lines
    assert "\tAPIServer [label=APIServer shape=component]" in lines
    assert "\tRedisCache [label=RedisCache shape=box3d]" in lines
