

from textual.containers import Horizontal
from textual.widgets import Static


class XCoordinateLabels(Horizontal):
    
    DEFAULT_CSS = """
    .x-coordinates{
        width:7;
        height:1;
        content-align:center middle;
        color:black;
    }
    
    XCoordinateLabels{
        width:auto;
        height:auto;
    }
    
    
    """
    
        
    
    def __init__(self,grid_size):
        super().__init__()
        self.grid_size = grid_size
        
    
    def compose(self):
        for x in range(self.grid_size):
            yield Static(f"[bold]{chr(ord('a') + x)}[/]",classes="x-coordinates")