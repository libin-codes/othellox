from textual.containers import Vertical
from textual.widgets import Static

class YCoordinateLabels(Vertical):
    
    DEFAULT_CSS = """
    YCoordinateLabels{
        width:auto;
        height:auto;
        color:black;
        padding-top:1;
    }
    .y-coordinates{
        width:3;
        height:3;
        content-align:center middle;
    }
    
    """
    
    
    def __init__(self,grid_size):
        super().__init__()
        self.grid_size = grid_size
        
    
    
    def compose(self):
        for y in range(self.grid_size):
            yield Static(f"[bold]{y+1}[/]",classes="y-coordinates")

