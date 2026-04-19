from textual.widget import Widget
from textual.app import ComposeResult
from textual.containers import  Vertical

from othellox.ui.board.board_header import GameBoardHeader
from othellox.ui.board.grid import Grid
from othellox.ui.board.x_coordinate_labels import XCoordinateLabels
from othellox.ui.board.y_coordinate_labels import YCoordinateLabels

    

class GameBoard(Widget):
    DEFAULT_CSS = """
    GameBoard{
        layout:horizontal;
        background:grey;
        width:auto;
        height:auto;
        padding-right:1;
        
        
    }
    
    #grid-container{
        layout:vertical;
        width:auto;
        height:auto;
        background:grey;
    }
    
    """
    
    
    def __init__(self,grid_size):
        super().__init__()
        self.grid_size = grid_size
       
    
    def compose(self)->ComposeResult:
        
        yield YCoordinateLabels(self.grid_size)
            
        # grid
        with Vertical(id="grid-container"):
            yield GameBoardHeader()
            yield Grid(self.grid_size)
            yield XCoordinateLabels(self.grid_size)
        
        