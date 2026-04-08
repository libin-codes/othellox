
from textual.widget import Widget
from textual.app import App,ComposeResult
from textual.containers import Center,Container


from othellox.game.type import Coordinate,BoardCell,Player
from othellox.ui.board.grid import Grid
from othellox.ui.board.cell import Cell,CellData
    

class GameBoard(Widget):
    CSS_PATH = """
    Board{
        width:auto;
        height:auto
    }
    
    """
    
    
    def __init__(self,grid_size):
        super().__init__()
        self.grid_size = grid_size
       
    
    def compose(self)->ComposeResult:
        yield Grid(self.grid_size)
        
        