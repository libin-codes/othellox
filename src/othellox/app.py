
from textual.app import App,ComposeResult
from textual.containers import Center,Container


from othellox.game.type import Coordinate,BoardCell,Player
from othellox.ui.board.grid import Grid
from othellox.ui.board.cell import Cell,CellData

from othellox.game.engine import OthelloEngine
from othellox.ui.board.board import Board

class Othello(App):
    
    def __init__(self):
        super().__init__()
        self.game = OthelloEngine(8)
        

    def compose(self)->ComposeResult:
        yield Board(8)
        
    def on_mount(self):
        self.update_cells()
        
        
    def find_cell(self,coordinate:Coordinate) -> Cell:
        cells = self.app.query(Cell)
        for cell in cells:
            if (cell.coordinate == coordinate):
                return cell
        raise 
        
        
        
    def update_cells(self):
        board = self.game.board
        size = self.game.board.size
        valid_moves = self.game.available_moves
        
        for x in range(size):
            for y in range(size):
                coord = Coordinate(x,y)
                cell_data = board[coord]
                cell_ui = self.find_cell(coord)
                
                match (cell_data):
                    case Player.WHITE:
                        cell_ui.data = CellData.WHITE
                    case Player.BLACK:
                        cell_ui.data = CellData.BLACK
                    case None:
                        cell_ui.data = CellData.EMPTY
                        
                cell_ui.is_valid_move = coord in valid_moves
            
            
    def on_cell_clicked(self,message:Cell.Clicked):
        self.game.move(message.coordinate)
        self.update_cells()
            
                    
if __name__ == "__main__":
    app = Othello()
    app.run()