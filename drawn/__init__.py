from dataclasses import dataclass
from typing import Optional
from graphviz import Digraph


@dataclass
class Node:
    name: str
    label: str


@dataclass
class Edge:
    src: Node
    dst: Node
    label: Optional[str] = None


class Reader:
    """
    Reads the input file and produces a list of flows and configs
    - flows are non-empty lines that do not start with a '%'
    - configs are non-empty lines that start with a '%'
    """

    def __init__(self, file_path: str):
        self.file_path = file_path
        self._lines = self._read_file()
        self.flows = self.read_flows()
        self.configs = self.read_configs()

    def _read_file(self) -> list[str]:
        with open(self.file_path, "r") as f:
            return f.readlines()

    def read_flows(self) -> list[str]:
        flow_lines = []
        lines = self._lines
        for line in lines:
            if line.strip() and not line.strip().startswith("%"):
                flow_lines.append(line.strip())
        return flow_lines

    def read_configs(self) -> list[str]:
        config_lines = []
        lines = self._lines
        for line in lines:
            if line.strip() and line.strip().startswith("%"):
                config_lines.append(line.strip())
        return config_lines


class Config:
    """
    Reads a list of config strings and parses them into a dictionary of config key-value pairs
    """

    def __init__(self, config_strings: Optional[list[str]] = None):
        # set defaults
        self.comment = "Flow"
        self.output_file = "flow"
        self.output_format = "svg"

        # Graph attributes
        self.graph_dpi = "300"
        self.graph_rankdir = "TB"
        self.graph_splines = "ortho"
        self.graph_pad = "0.2"
        self.graph_nodesep = "1"
        self.graph_ranksep = "0.8"

        # Node attributes
        self.node_margin = "0.15,0.1"
        self.node_fontname = "Courier"
        self.node_fontsize = "12"
        self.node_shape = "box"

        # Edge attributes
        self.edge_fontname = "Courier"
        self.edge_fontsize = "12"
        self.edge_arrowhead = "normal"
        self.edge_penwidth = "0.8"

        # Theme
        self.theme = "light"  # default theme
        self.apply_theme()


        # override defaults if config strings are provided
        if config_strings:
            for config_string in config_strings:
                config = config_string.removeprefix("%").strip()
                key, value = config.split(":")
                key = key.strip()
                value = value.strip()

                if key == "output_file":
                    self.output_file = value
                elif key == "output_format":
                    self.output_format = value
                elif key == "comment":
                    self.comment = value

                # Themes
                elif key == "theme":
                    self.theme = value
                    self.apply_theme()

                # Graph attributes
                elif key == "graph_dpi":
                    self.graph_dpi = value
                elif key == "graph_rankdir":
                    self.graph_rankdir = value
                elif key == "graph_splines":
                    self.graph_splines = value
                elif key == "graph_pad":
                    self.graph_pad = value
                elif key == "graph_nodesep":
                    self.graph_nodesep = value
                elif key == "graph_ranksep":
                    self.graph_ranksep = value
                elif key == "graph_bgcolor":
                    self.graph_bgcolor = value

                # Node attributes
                elif key == "node_fontcolor":
                    self.node_fontcolor = value
                elif key == "node_shape":
                    self.node_shape = value
                elif key == "node_margin":
                    self.node_margin = value
                elif key == "node_fontname":
                    self.node_fontname = value
                elif key == "node_fontsize":
                    self.node_fontsize = value
                elif key == "node_style":
                    self.node_style = value
                elif key == "node_fillcolor":
                    self.node_fillcolor = value

                # Edge attributes
                elif key == "edge_color":
                    self.edge_color = value
                elif key == "edge_fontcolor":
                    self.edge_fontcolor = value
                elif key == "edge_fontname":
                    self.edge_fontname = value
                elif key == "edge_fontsize":
                    self.edge_fontsize = value
                elif key == "edge_arrowhead":
                    self.edge_arrowhead = value
                elif key == "edge_penwidth":
                    self.edge_penwidth = value

                # Unsupported
                else:
                    raise ValueError(f"Invalid config: {config}")
            
    def apply_theme(self):        
        if self.theme == "dark":
            self.graph_bgcolor = "black"
            self.node_fillcolor = "black"
            self.node_fontcolor = "white"
            self.node_color = "white"
            self.node_style = "filled"
            self.edge_color = "white"
            self.edge_fontcolor = "white"
        else:  # default to light theme for any other value
            self.graph_bgcolor = "white"
            self.node_color = "black"
            self.node_fillcolor = "white"
            self.node_fontcolor = "black"
            self.node_style = "filled"
            self.edge_color = "black"
            self.edge_fontcolor = "black"

class Parser:
    """
    Parses the list of 'flows' and produces a list of Node and Edge objects
    """

    def __init__(self, flows: list[str]):
        self.flows = flows

    def parse(self) -> tuple[list[Node], list[Edge]]:
        edges = []
        nodes = {}
        for flow in self.flows:
            parts = flow.strip().split()
            i = 0
            while i < len(parts) - 2:
                src = parts[i]
                arrow = parts[i + 1]
                dst = parts[i + 2]
                nodes[src] = Node(src, src)
                nodes[dst] = Node(dst, dst)

                if arrow == "-->":
                    edge = Edge(nodes[src], nodes[dst], None)
                elif arrow.startswith("-(") and arrow.endswith(")->"):
                    arrow_label = arrow.split("-(")[1].split(")->")[0]
                    edge = Edge(nodes[src], nodes[dst], arrow_label)
                else:
                    raise ValueError(f"Unexpected arrow syntax: {arrow}")
                edges.append(edge)
                i += 2
        return nodes.values(), edges


class Compiler:
    """
    Takes Node and Edge objects and produces DOT source
    """

    def __init__(
        self,
        nodes: list[Node],
        edges: list[Edge],
        config: Optional[Config] = None,
    ):
        self.nodes = nodes
        self.edges = edges
        if not config:
            config = Config()
        self.config = config
        self.dot = Digraph(comment=config.comment, format=config.output_format)

    def _set_default_attributes(self):

        # Graph attributes
        self.dot.attr(dpi=self.config.graph_dpi)
        self.dot.attr(bgcolor=self.config.graph_bgcolor)
        self.dot.attr(rankdir=self.config.graph_rankdir)
        self.dot.attr(splines=self.config.graph_splines)
        self.dot.attr(pad=self.config.graph_pad)
        self.dot.attr(nodesep=self.config.graph_nodesep)
        self.dot.attr(ranksep=self.config.graph_ranksep)

        # Node attributes
        self.dot.node_attr["fontname"] = self.config.node_fontname
        self.dot.node_attr["fontsize"] = self.config.node_fontsize
        self.dot.node_attr["fontcolor"] = self.config.node_fontcolor
        self.dot.node_attr["shape"] = self.config.node_shape
        self.dot.node_attr["style"] = self.config.node_style
        self.dot.node_attr["fillcolor"] = self.config.node_fillcolor
        self.dot.node_attr["color"] = self.config.node_color
        self.dot.node_attr["margin"] = self.config.node_margin

        # Edge attributes
        self.dot.edge_attr["color"] = self.config.edge_color
        self.dot.edge_attr["arrowhead"] = self.config.edge_arrowhead
        self.dot.edge_attr["penwidth"] = self.config.edge_penwidth
        self.dot.edge_attr["fontname"] = self.config.edge_fontname
        self.dot.edge_attr["fontsize"] = self.config.edge_fontsize
        self.dot.edge_attr["fontcolor"] = self.config.edge_fontcolor

    def compile(self):
        for node in self.nodes:
            self.dot.node(node.name, label=node.label)
        for e in self.edges:
            if e.label:
                self.dot.edge(e.src.name, e.dst.name, xlabel=e.label)
            else:
                self.dot.edge(e.src.name, e.dst.name)
        return self.dot.source

    def render(self):
        self._set_default_attributes()
        self.compile()
        self.dot.render(self.config.output_file, view=False, cleanup=True)
