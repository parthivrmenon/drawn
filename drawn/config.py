from typing import Optional


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
        self.node_style = "filled"

        # Edge attributes
        self.edge_fontname = "Courier"
        self.edge_fontsize = "12"
        self.edge_arrowhead = "normal"
        self.edge_penwidth = "0.8"

        # Theme
        self.theme = "light"
        self.apply_theme()

        # Auto-shapes
        self.auto_shapes = True

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

                # Theme system
                elif key == "theme":
                    self.theme = value
                    self.apply_theme()

                # Auto-shapes
                elif key == "auto_shapes":
                    self.auto_shapes = value.lower() in ("true", "yes", "1", "on")

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
        """Apply theme settings"""
        if self.theme == "dark":
            self.graph_bgcolor = "black"
            self.node_fillcolor = "black"
            self.node_fontcolor = "white"
            self.node_color = "white"
            self.edge_color = "white"
            self.edge_fontcolor = "white"

        elif self.theme == "matrix":
            self.graph_bgcolor = "black"
            self.node_fillcolor = "#001100"  # Very dark green
            self.node_fontcolor = "#00FF00"  # Bright green text
            self.node_color = "#00FF00"  # Bright green border
            self.edge_color = "#00FF00"  # Bright green lines
            self.edge_fontcolor = "#00FF00"  # Bright green edge text

        else:  # light (default)
            self.graph_bgcolor = "white"
            self.node_fillcolor = "white"
            self.node_fontcolor = "black"
            self.node_color = "black"
            self.edge_color = "black"
            self.edge_fontcolor = "black"
