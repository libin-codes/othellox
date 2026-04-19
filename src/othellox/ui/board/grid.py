from textual.widget import Widget
from textual.containers import Container,Center, Horizontal, Vertical
from textual.widgets import Placeholder, Static
from othellox.game.board import Board
from othellox.ui.board.board_header import GameBoardHeader
from othellox.ui.board.cell import Cell, CellData,Shade
from othellox.game.type import Coordinate,BoardCell, Player
from othellox.ui.board.x_coordinate_labels import XCoordinateLabels
from othellox.ui.board.y_coordinate_labels import YCoordinateLabels

class Grid(Widget):
    
    DEFAULT_CSS = '''
    Grid{
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
        self.cells:dict[str,Cell] = {}
        
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
        
    def get_cell(self, coord: str) -> Cell:
        return self.cells[coord]
    
    
    def sync(self,board:dict[str,Player | None]):
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
        
           
    
    def mark_valid_moves(self, valid_moves):

        for coord, cell in self.cells.items():
            cell.is_valid_move = coord in valid_moves
            
    def clear_valid_moves(self):
        for cell in self.cells.values():
            cell.is_valid_move = False
                
                
    def highlight_cell(self,coordinate:str):
        self.get_cell(coordinate).highlight = True
        
    def clear_highlight(self):
        for cell in self.cells.values():
            cell.highlight = False