from drawn.model.digraph import Config, DirectedGraph, Edge, Node


class Reader:
    """
    Takes a filepath and return a Digraph
    """

    def __init__(self, filepath: str):
        self.filepath = filepath

    def parse_config(self, config_lines: list[str]) -> Config:
        # init with default values
        config = Config(
            comment="Flow",
            output_file="flow",
            output_format="svg",
            theme="light",
        )
        for line in config_lines:
            line = line.strip()
            config_line = line.removeprefix("%").strip()
            key, value = config_line.split(":")
            key = key.strip()
            value = value.strip()
            if key == "theme":
                config.theme = value
            elif key == "output_file":
                config.output_file = value
            elif key == "output_format":
                config.output_format = value
            elif key == "comment":
                config.comment = value
            else:
                raise ValueError(f"Unexpected config key: {key}")

        print(config)
        return config

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

        nodes, edges = self.parse(flow_lines)
        config = self.parse_config(config_lines)

        return DirectedGraph(
            nodes=nodes,
            edges=edges,
            config=config,
        )
