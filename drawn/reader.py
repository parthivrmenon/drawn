from drawn.model.digraph import DirectedGraph
from drawn.parser import Parser


class Reader:
    """Reads .drawn files from the filesystem.
    
    This class handles file I/O and delegates parsing to the Parser.
    """

    def __init__(self, filepath: str):
        """Initialize reader with a file path.
        
        Args:
            filepath: Path to the .drawn file
        """
        self.filepath = filepath

    def read(self) -> DirectedGraph:
        """Read and parse the .drawn file.
        
        Returns:
            DirectedGraph object representing the diagram
            
        Raises:
            FileNotFoundError: If file doesn't exist
            ValueError: If file format is invalid
        """
        with open(self.filepath, "r") as f:
            content = f.read()
        return Parser.parse(content)
