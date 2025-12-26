"""Theme configurations for Drawn diagrams."""

COMMON_ATTRIBUTES = {
    "graph": {
        "dpi": "300",
        "rankdir": "TB",
        "splines": "ortho",
        "pad": "0.2",
        "nodesep": "1",
        "ranksep": "0.8",
    },
    "node": {
        "margin": "0.15,0.1",
        "fontname": "Courier",
        "fontsize": "12",
        "shape": "box",
        "style": "filled",
    },
    "edge": {
        "fontname": "Courier",
        "fontsize": "12",
        "arrowhead": "normal",
        "penwidth": "0.8",
    },
}

THEME_CONFIGS = {
    "light": {
        "graph": {"bgcolor": "white"},
        "node": {"fillcolor": "white", "fontcolor": "black", "color": "black"},
        "edge": {"color": "black", "fontcolor": "black"},
    },
    "dark": {
        "graph": {"bgcolor": "black"},
        "node": {"fillcolor": "black", "fontcolor": "white", "color": "white"},
        "edge": {"color": "white", "fontcolor": "white"},
    },
    "matrix": {
        "graph": {"bgcolor": "black"},
        "node": {"fillcolor": "#001100", "fontcolor": "#00FF00", "color": "#00FF00"},
        "edge": {"color": "#00FF00", "fontcolor": "#00FF00"},
    },
}


def get_theme(theme: str):
    if theme not in THEME_CONFIGS:
        raise ValueError(f"Invalid theme: {theme}")
    config = {}
    for category in ["graph", "node", "edge"]:
        config[category] = {
            **COMMON_ATTRIBUTES[category],
            **THEME_CONFIGS[theme][category],
        }
    return config
