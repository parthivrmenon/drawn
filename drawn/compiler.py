from typing import Optional

from graphviz import Digraph

from .config import Config
from .models import Edge, Node
from .shapes import get_auto_shape_for_node


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
            if self.config.auto_shapes:
                node_shape = get_auto_shape_for_node(node.name)
                self.dot.node(node.name, label=node.label, shape=node_shape)
            else:
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
