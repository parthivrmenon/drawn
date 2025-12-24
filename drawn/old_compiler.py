from graphviz import Digraph

from drawn.model.digraph import DirectedGraph


class Compiler:
    def __init__(self, digraph: DirectedGraph):
        self.digraph = digraph
        self.dot = Digraph(
            comment=digraph.config.comment, format=digraph.config.output_format
        )
        
    def set_graph_attributes(self, theme: str):
        self.dot.attr(dpi="300")
        self.dot.attr(rankdir="TB")
        self.dot.attr(splines="ortho")
        self.dot.attr(pad="0.2")
        self.dot.attr(nodesep="1")
        self.dot.attr(ranksep="0.8")
        if theme == "light":
            self.dot.attr(bgcolor="white")
        elif theme == "dark":
            self.dot.attr(bgcolor="black")
        elif theme == "matrix":
            self.dot.attr(bgcolor="black")
        else:
            raise ValueError(f"Unexpected theme: {theme}")

    def set_node_attributes(self, theme: str):
        self.dot.node_attr["margin"] = "0.15,0.1"
        self.dot.node_attr["fontname"] = "Courier"
        self.dot.node_attr["fontsize"] = "12"
        self.dot.node_attr["shape"] = "box"
        self.dot.node_attr["style"] = "filled"
        if theme == "light":
            self.dot.node_attr["fillcolor"] = "white"
            self.dot.node_attr["fontcolor"] = "black"
            self.dot.node_attr["color"] = "black"
        elif theme == "dark":
            self.dot.node_attr["fillcolor"] = "black"
            self.dot.node_attr["fontcolor"] = "white"
            self.dot.node_attr["color"] = "white"
        elif theme == "matrix":
            self.dot.node_attr["fillcolor"] = "#001100"
            self.dot.node_attr["fontcolor"] = "#00FF00"
            self.dot.node_attr["color"] = "#00FF00"
        else:
            raise ValueError(f"Unexpected theme: {theme}")

    def set_edge_attributes(self, theme: str):
        self.dot.edge_attr["fontname"] = "Courier"
        self.dot.edge_attr["fontsize"] = "12"
        self.dot.edge_attr["arrowhead"] = "normal"
        self.dot.edge_attr["penwidth"] = "0.8"
        if theme == "light":
            self.dot.edge_attr["color"] = "black"
            self.dot.edge_attr["fontcolor"] = "black"
        elif theme == "dark":
            self.dot.edge_attr["color"] = "white"
            self.dot.edge_attr["fontcolor"] = "white"
        elif theme == "matrix":
            self.dot.edge_attr["color"] = "#00FF00"
            self.dot.edge_attr["fontcolor"] = "#00FF00"
        else:
            raise ValueError(f"Unexpected theme: {theme}")

    def compile(self):
        """
        produces DOT source
        """
        self.set_graph_attributes(self.digraph.config.theme)
        self.set_node_attributes(self.digraph.config.theme)
        self.set_edge_attributes(self.digraph.config.theme)

        for node in self.digraph.nodes:
            self.dot.node(node.name, label=node.label)
        for edge in self.digraph.edges:
            if edge.label:
                self.dot.edge(edge.src.name, edge.dst.name, xlabel=edge.label)
            else:
                self.dot.edge(edge.src.name, edge.dst.name)
        return self.dot.source

    def render(self):
        self.compile()
        self.dot.render(self.digraph.config.output_file, view=False, cleanup=True)
