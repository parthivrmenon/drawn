from graphviz import Digraph

from drawn.model.digraph import DirectedGraph
from drawn.shapes import get_auto_shape_for_node
from drawn.themes import get_theme


class Compiler:
    """Compiles DirectedGraph objects into Graphviz DOT format.
    
    This class provides static methods for transforming DirectedGraph data
    structures into DOT source code and rendered diagram files.
    """

    @staticmethod
    def compile(digraph: DirectedGraph) -> str:
        """Compile a DirectedGraph into DOT source code.
        
        Args:
            digraph: The DirectedGraph to compile
            
        Returns:
            str: DOT source code
            
        Raises:
            ValueError: If theme is not recognized
        """
        dot = Digraph(
            comment=digraph.config.comment,
            format=digraph.config.output_format
        )
        
        # Apply theme attributes
        Compiler._apply_attributes(dot, digraph.config.theme)
        
        # Add nodes
        for node in digraph.nodes:
            node_attrs = {"label": node.label}
            
            # Apply auto-shape selection if enabled
            if digraph.config.auto_shapes:
                node_attrs["shape"] = get_auto_shape_for_node(node.name)
            else:
                node_attrs["shape"] = "box"
            
            dot.node(name=node.name, **node_attrs)
        
        # Add edges
        for edge in digraph.edges:
            if edge.label:
                dot.edge(edge.src.name, edge.dst.name, xlabel=edge.label)
            else:
                dot.edge(edge.src.name, edge.dst.name)
        
        return dot.source

    @staticmethod
    def render(digraph: DirectedGraph) -> None:
        """Compile and render a DirectedGraph to a file.
        
        Args:
            digraph: The DirectedGraph to render
            
        Raises:
            ValueError: If theme is not recognized
        """
        dot = Digraph(
            comment=digraph.config.comment,
            format=digraph.config.output_format
        )
        
        # Apply theme attributes
        Compiler._apply_attributes(dot, digraph.config.theme)
        
        # Add nodes
        for node in digraph.nodes:
            node_attrs = {"label": node.label}
            
            # Apply auto-shape selection if enabled
            if digraph.config.auto_shapes:
                node_attrs["shape"] = get_auto_shape_for_node(node.name)
            else:
                node_attrs["shape"] = "box"
            
            dot.node(name=node.name, **node_attrs)
        
        # Add edges
        for edge in digraph.edges:
            if edge.label:
                dot.edge(edge.src.name, edge.dst.name, xlabel=edge.label)
            else:
                dot.edge(edge.src.name, edge.dst.name)
        
        dot.render(digraph.config.output_file, view=False, cleanup=True)

    @staticmethod
    def _apply_attributes(dot: Digraph, theme: str) -> None:
        """Apply theme attributes to a Digraph instance.
        
        Args:
            dot: The Digraph instance to modify
            theme: Theme name (e.g., 'light', 'dark', 'matrix')
            
        Raises:
            ValueError: If theme is not recognized
        """
        config = get_theme(theme)

        # Note: graphviz uses different APIs for different attribute types:
        # - Graph attrs: use .attr() method with keyword args
        # - Node/Edge attrs: use ._attr dict with direct assignment

        for key, val in config["graph"].items():
            dot.attr(**{key: val})
        for key, val in config["node"].items():
            dot.node_attr[key] = val
        for key, val in config["edge"].items():
            dot.edge_attr[key] = val
