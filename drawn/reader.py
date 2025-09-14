class Reader:
    """
    Reads the input file and produces a list of flows and configs
    - flows are non-empty lines that do not start with a '%'
    - configs are non-empty lines that start with a '%'
    """

    def __init__(self, file_path: str):
        self.file_path = file_path
        self._lines = self._read_file()
        self.flows = self.read_flows()
        self.configs = self.read_configs()

    def _read_file(self) -> list[str]:
        with open(self.file_path, "r") as f:
            return f.readlines()

    def read_flows(self) -> list[str]:
        flow_lines = []
        lines = self._lines
        for line in lines:
            if line.strip() and not line.strip().startswith("%"):
                flow_lines.append(line.strip())
        return flow_lines

    def read_configs(self) -> list[str]:
        config_lines = []
        lines = self._lines
        for line in lines:
            if line.strip() and line.strip().startswith("%"):
                config_lines.append(line.strip())
        return config_lines
