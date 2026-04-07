from textual.widget import Widget
from textual.containers import Container,Center
from othellox.ui.board.cell import Cell,Shade
from othellox.game.type import Coordinate,BoardCell

class Grid(Widget):
    
    DEFAULT_CSS = '''
    Grid{
        width:auto;
        height:auto;
    }
    #grid-container{
        layout:vertical;
        width:auto;
        height:auto;
    }
    .grid-rows{
        layout:horizontal;
        width:auto;
        height:auto;
    }
    
    '''
    
    
    def __init__(self,grid_size:int):
        super().__init__()
        self.grid_size = grid_size
        
    def compose(self):
        with Container(id="grid-container"):
            shade = Shade.LIGHT
            for y in range(self.grid_size-1,-1,-1):
                with Container(classes="grid-rows"):
                    for x in range(self.grid_size):
                        coordinate = Coordinate(x,y)
                        yield Cell(coordinate,shade)
                        shade = Shade.LIGHT if shade==Shade.DARK else Shade.DARK
                shade = Shade.LIGHT if shade==Shade.DARK else Shade.DARK
                    
                        

                        
                    
            
                
        
        
    