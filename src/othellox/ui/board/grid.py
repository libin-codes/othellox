from textual.widget import Widget
from textual.containers import Container,Center, Horizontal, Vertical
from textual.widgets import Placeholder, Static
from othellox.game.board import Board
from othellox.ui.board.cell import Cell, CellData,Shade
from othellox.game.type import Coordinate,BoardCell, Player

class Grid(Widget):
    
    DEFAULT_CSS = '''
    Grid{
        layout:horizontal;
        width:auto;
        height:auto;
        padding-top:1;
        padding-right:1;
        background:grey;
        outline-top:thick transparent;
        
       
    }
    #grid-container{
        layout:vertical;
        width:auto;
        height:auto;
        background:grey;
     
    }
    .grid-rows{
        width:auto;
        height:auto;
    }
    .y-coordinates{
        width:3;
        height:3;
        content-align:center middle;
      
    }
    
    .x-coordinates{
        width:7;
        height:1;
        content-align:center middle;
        color:black;
    }
    
    #x-coordinate-container{
        width:auto;
        height:auto;
    }
    
    #y-coordinate-container{
        width:auto;
        height:auto;
        color:black;
    }
    
    
    '''
    
    
    def __init__(self,grid_size:int):
        super().__init__()
        self.grid_size = grid_size
        self.cells:dict[Coordinate,Cell] = {}
        
    def compose(self):
            # y-coordinate
            with Vertical(id="y-coordinate-container"):
                for y in range(self.grid_size):
                    yield Static(f"[bold]{y+1}[/]",classes="y-coordinates")
            # grid
            with Vertical(id="grid-container"):
                for y in range(self.grid_size-1,-1,-1):
                    with Horizontal(classes="grid-rows"):
                        for x in range(self.grid_size):
                            coordinate = Coordinate(x,y)
                            shade = Shade((x + y) % 2)
                            yield Cell(coordinate,shade)
            # x-coordinate
                with Horizontal(id="x-coordinate-container"):
                    for x in range(self.grid_size):
                        yield Static(f"[bold]{chr(ord('a') + x)}[/]",classes="x-coordinates")
                                 
    def on_mount(self):
        self.cells = {
            cell.coordinate: cell
            for cell in self.query(Cell)
        }
        
    def get_cell(self, coord: Coordinate) -> Cell:
        return self.cells[coord]
    
    
    def sync(self,board:Board):
        """syncs the engine board with ui board

        Args:
            board (Board): The game engine board
            valid_moves (list[Coordinate]): list of valid moves
        """
        for coord, cell_ui in self.cells.items():
            cell_data = board[coord]    
            match (cell_data):
                case Player.WHITE:
                    cell_ui.data = CellData.WHITE
                case Player.BLACK:
                    cell_ui.data = CellData.BLACK
                case None:
                    cell_ui.data = CellData.EMPTY
        
           
    
    def show_valid_moves(self, valid_moves):

        for coord, cell in self.cells.items():
            cell.is_valid_move = coord in valid_moves
            
    def clear_valid_moves(self):
        for cell in self.cells.values():
            cell.is_valid_move = False
                
                
    def highlight_cell(self,coordinate:Coordinate):
        self.get_cell(coordinate).highlight = True
        
    def clear_highlight(self):
        for cell in self.cells.values():
            cell.highlight = False