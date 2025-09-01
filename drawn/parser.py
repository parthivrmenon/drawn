
def read_file(file_path:str) -> list[str]:
    with open(file_path, "r") as f:
        return f.readlines()

def parse(flows:list[str]) -> list[tuple[str, str]]:
    """
    Parse the list of flow lines into edges

    """
    edges = []

    for flow in flows:
        nodes = flow.strip().split(" --> ")
        for i in range(len(nodes) - 1):
            edges.append((nodes[i], nodes[i + 1]))
    return edges