from graphviz import Digraph



def render_graphviz(edges: list[tuple[str, str]], output_file:str, output_format:str="svg"):
    """
    Render the graphviz diagram

    """
    dot = Digraph(comment="Drawn Flow", format=output_format)
    dot.attr(dpi='150')
    dot.attr(rankdir="LR")

    all_nodes = set()
    for edge in edges:
        all_nodes.add(edge[0])
        all_nodes.add(edge[1])
    
    for node in all_nodes:
        dot.node(node, shape="box", style="filled", fontname="Arial", fillcolor="lightblue")
    
    for edge in edges:
        dot.edge(edge[0], edge[1])
    
    dot.render(output_file, view=False)
    return output_file

