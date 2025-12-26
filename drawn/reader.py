from drawn.model.digraph import Config, DirectedGraph, Edge, Node
from drawn.shapes import get_auto_shape_for_node


class Reader:
    """
    Implements the reader for .drawn files
    """

    def __init__(self, filepath: str):
        self.filepath = filepath
        self.config = None  # will be set in parse_config

    def parse_config(self, config_lines: list[str]) -> Config:
        """Parse configuration lines into a Config object.
        
        Extracts key-value pairs from lines starting with '%' and delegates
        validation to the Config dataclass.
        
        Args:
            config_lines: List of lines from the .drawn file
            
        Returns:
            Config object with parsed settings
            
        Raises:
            ValueError: If configuration contains invalid keys or values
        """
        config_dict = {}
        for line in config_lines:
            line = line.strip()
            if not line or not line.startswith("%"):
                continue
            line = line.removeprefix("%").strip()
            if ":" not in line:
                continue
            key, value = line.split(":", 1)  # maxsplit=1 for values containing ":"
            key = key.strip()
            value = value.strip()
            
            # Type conversion for boolean fields
            if key == "auto_shapes":
                value = value.lower() in ["true", "yes", "1"]
            
            config_dict[key] = value
        
        try:
            return Config(**config_dict)
        except TypeError as e:
            raise ValueError(f"Invalid configuration: {e}") from e

    def parse(self, flows: list[str]) -> tuple[list[Node], list[Edge]]:
        edges = []
        nodes = {}
        for flow in flows:
            parts = flow.strip().split()
            i = 0
            while i < len(parts) - 2:
                src = parts[i]
                arrow = parts[i + 1]
                dst = parts[i + 2]

                if src not in nodes:
                    if self.config.auto_shapes:
                        src_shape = get_auto_shape_for_node(src)
                    else:
                        src_shape = get_auto_shape_for_node("default")
                    nodes[src] = Node(src, src, src_shape)
                if dst not in nodes:
                    if self.config.auto_shapes:
                        dst_shape = get_auto_shape_for_node(dst)
                    else:
                        dst_shape = get_auto_shape_for_node("default")
                    nodes[dst] = Node(dst, dst, dst_shape)
                if arrow == "-->" or arrow == "->":
                    edge = Edge(nodes[src], nodes[dst], None)
                elif arrow.startswith("-(") and arrow.endswith(")->"):
                    arrow_label = arrow.split("-(")[1].split(")->")[0]
                    edge = Edge(nodes[src], nodes[dst], arrow_label)
                else:
                    raise ValueError(f"Unexpected arrow syntax: {arrow}")
                edges.append(edge)
                i += 2
        return nodes.values(), edges

    def read(self) -> DirectedGraph:
        flow_lines = []
        config_lines = []
        with open(self.filepath, "r") as f:
            lines = f.readlines()

        for line in lines:
            line = line.strip()

            # if line is not a 'config'
            if not line.startswith("%"):
                flow_lines.append(line)
            else:
                config_lines.append(line)
        self.config = self.parse_config(config_lines)
        nodes, edges = self.parse(flow_lines)

        return DirectedGraph(
            nodes=nodes,
            edges=edges,
            config=self.config,
        )
