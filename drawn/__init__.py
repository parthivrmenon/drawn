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


class Parser:
    """
    Parses the input file and produces a list of Node and Edge objects
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
        output_format: str = "svg",
        comment: str = "Flow",
        output_file: str = "drawn_flow",
    ):
        self.nodes = nodes
        self.edges = edges
        self.output_format = output_format
        self.comment = comment
        self.dot = Digraph(comment=comment, format=output_format)
        self.output_file = output_file

    def _set_default_attributes(self):

        # Graph attributes
        self.dot.attr(dpi="300")
        self.dot.attr(bgcolor="transparent")
        self.dot.attr(rankdir="TB", splines="ortho")
        self.dot.attr(pad="0.2", nodesep="1", ranksep="0.8")

        # Node attributes
        self.dot.node_attr["fontname"] = "Courier"
        self.dot.node_attr["fontcolor"] = "white"
        self.dot.node_attr["shape"] = "box"
        self.dot.node_attr["style"] = "filled"
        self.dot.node_attr["fillcolor"] = "transparent"
        self.dot.node_attr["color"] = "white"
        self.dot.node_attr["margin"] = "0.15,0.1"

        # Edge attributes
        self.dot.edge_attr["color"] = "black"
        self.dot.edge_attr["arrowhead"] = "normal"
        self.dot.edge_attr["penwidth"] = "0.8"
        self.dot.edge_attr["fontname"] = "Courier"
        self.dot.edge_attr["color"] = "white"
        self.dot.edge_attr["fontcolor"] = "white"

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
        self.dot.render(self.output_file, view=False, cleanup=True)
