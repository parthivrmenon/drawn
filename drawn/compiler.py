from graphviz import Digraph

from drawn.model.digraph import DirectedGraph
from drawn.themes import get_theme


class Compiler:
    """
    Implements the compiler for .drawn files
    """

    def __init__(self, digraph: DirectedGraph):
        self.digraph = digraph
        self.dot = Digraph(
            comment=digraph.config.comment, format=digraph.config.output_format
        )

    def apply_attributes(self, theme: str):
        """Apply all theme attributes (graph, node, edge) to the diagram.

        Merges common attributes with theme-specific styling and applies them
        to the graphviz Digraph instance.

        Args:
            theme: Theme name (e.g., 'light', 'dark', 'matrix')

        Raises:
            ValueError: If theme is not recognized
        """
        config = get_theme(theme)

        # Note: graphviz uses different APIs for different attribute types:
        # - Graph attrs: use .attr() method with keyword args
        # - Node/Edge attrs: use ._attr dict with direct assignment

        for key, val in config["graph"].items():
            self.dot.attr(**{key: val})
        for key, val in config["node"].items():
            self.dot.node_attr[key] = val
        for key, val in config["edge"].items():
            self.dot.edge_attr[key] = val

    def compile(self):
        """
        produces DOT source
        """
        self.apply_attributes(self.digraph.config.theme)

        for node in self.digraph.nodes:
            node_attrs = {"label": node.label}
            if node.shape:
                node_attrs["shape"] = node.shape
            self.dot.node(name=node.name, **node_attrs)
        for edge in self.digraph.edges:
            if edge.label:
                self.dot.edge(edge.src.name, edge.dst.name, xlabel=edge.label)
            else:
                self.dot.edge(edge.src.name, edge.dst.name)
        return self.dot.source

    def render(self):
        self.compile()
        self.dot.render(self.digraph.config.output_file, view=False, cleanup=True)
