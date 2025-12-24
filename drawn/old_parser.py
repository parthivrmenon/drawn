from .models import Edge, Node


class Parser:
    """
    Parses the list of 'flows' and produces a list of Node and Edge objects
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
