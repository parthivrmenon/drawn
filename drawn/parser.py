from drawn.model.digraph import Config, DirectedGraph, Edge, Node


class Parser:
    """Parses .drawn text content into DirectedGraph objects.
    
    This class handles the pure transformation from text to data structures,
    with no I/O dependencies.
    """

    @staticmethod
    def parse(content: str) -> DirectedGraph:
        """Parse .drawn content into a DirectedGraph.
        
        Args:
            content: The complete .drawn file content as a string
            
        Returns:
            DirectedGraph object representing the diagram
            
        Raises:
            ValueError: If content format is invalid
        """
        lines = content.splitlines()
        
        # Separate config and flow lines
        config_lines = [l for l in lines if l.strip().startswith("%")]
        flow_lines = [l for l in lines if not l.strip().startswith("%")]
        
        config = Parser._parse_config(config_lines)
        nodes, edges = Parser._parse_flows(flow_lines, config)
        
        return DirectedGraph(nodes=nodes, edges=edges, config=config)

    @staticmethod
    def _parse_config(config_lines: list[str]) -> Config:
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

    @staticmethod
    def _parse_flows(flows: list[str], config: Config) -> tuple[list[Node], list[Edge]]:
        """Parse flow lines into nodes and edges.
        
        Args:
            flows: List of flow definition lines
            config: Configuration object for parsing options
            
        Returns:
            Tuple of (nodes, edges)
            
        Raises:
            ValueError: If arrow syntax is invalid
        """
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
                    nodes[src] = Node(src, src)
                if dst not in nodes:
                    nodes[dst] = Node(dst, dst)
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
