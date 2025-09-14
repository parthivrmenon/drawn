from dataclasses import dataclass
from typing import Optional


@dataclass
class Node:
    name: str
    label: str


@dataclass
class Edge:
    src: Node
    dst: Node
    label: Optional[str] = None
