from dataclasses import dataclass
from typing import List, Optional


@dataclass
class Config:
    comment: str = "Flow"
    output_file: str = "flow"
    output_format: str = "svg"
    theme: str = "light"
    auto_shapes: bool = True


@dataclass
class Node:
    name: str
    label: str
    shape: Optional[str] = None


@dataclass
class Edge:
    src: Node
    dst: Node
    label: Optional[str] = None


@dataclass
class DirectedGraph:
    nodes: List[Node]
    edges: List[Edge]
    config: Config
