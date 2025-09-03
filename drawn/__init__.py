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
        self.dot.attr(dpi="150")
        self.dot.attr(pad="0.2", nodesep="0.3", ranksep="0.4")
        self.dot.attr(rankdir="LR", splines="ortho")
        self.dot.node_attr["fontname"] = "Courier"
        self.dot.node_attr["fontcolor"] = "black"
        self.dot.node_attr["fontsize"] = "10"
        self.dot.node_attr["fillcolor"] = "white"
        self.dot.node_attr["penwidth"] = "0.5"
        self.dot.node_attr["shape"] = "box"
        self.dot.node_attr["style"] = "filled"
        self.dot.node_attr["fillcolor"] = "#f5f5f5"
        self.dot.edge_attr["arrowhead"] = "normal"
        self.dot.edge_attr["penwidth"] = "0.5"
        self.dot.edge_attr["arrowsize"] = "0.5"
        self.dot.edge_attr["fontname"] = "Courier"
        self.dot.edge_attr["fontsize"] = "8"

    def compile(self):
        for node in self.nodes:
            self.dot.node(node.name, label=node.label)
        for e in self.edges:
            if e.label:
                self.dot.edge(e.src.name, e.dst.name, label=e.label)
            else:
                self.dot.edge(e.src.name, e.dst.name)
        return self.dot.source

    def render(self):
        self._set_default_attributes()
        self.dot.render(self.output_file, view=False)
