from textual.widget import Widget
from textual.containers import Horizontal
from othellox.ui.board.cell import Cell, CellData,Shade
from othellox.game.type import  Player, Square


class GameGrid(Widget):
    
    DEFAULT_CSS = '''
    GameGrid{
        width:auto;
        height:auto;
       
    }
   
    .grid-rows{
        width:auto;
        height:auto;
    }
    '''
    
    
    def __init__(self,grid_size:int):
        super().__init__()
        self.grid_size = grid_size
        self.cells:dict[Square,Cell] = {}
        
    def compose(self):
        
        y_coordinates = range(self.grid_size,0,-1)
        x_coordinates = [chr(ord("a") + i) for i in range(self.grid_size)]
        
        for y in y_coordinates:
            with Horizontal(classes="grid-rows"):
                for x in x_coordinates:
                    shade = Shade((ord(x) + y) % 2)
                    yield Cell(f"{x}{y}",shade)
        
                                 
    def on_mount(self):
        self.cells = {
            cell.coordinate: cell
            for cell in self.query(Cell)
        }

        