
from textual import on
from textual.app import App,ComposeResult
from textual.containers import Container
from textual.events import MouseMove
from textual.widgets import Footer, Input


from othellox.game.type import Player, Square
from othellox.ui.board.board_header import GameBoardHeader
from othellox.ui.board.grid import GameGrid
from othellox.ui.board.cell import Cell

from othellox.game.engine import OthelloEngine
from othellox.ui.board.game_board import GameBoard
from othellox.ui.move_history import MoveHistory
from othellox.ui.move_selection import MoveSelection

class Othello(App):
    
    DEFAULT_CSS = """
    Screen{
        width:100%;
        height:100%;
        align:center middle;
        background:$background;
        hatch: left green 10%;
        
    }
    #app-container{
        width:auto;
        height:auto;
        layout:horizontal;
    }
    
    #side-panel{
        width:auto;
        height:100%;
        align:center bottom;
    }
    
   
    
    """
    
    
    def __init__(self):
        super().__init__()
        self.game = OthelloEngine(8)


    def compose(self)->ComposeResult:
        with Container(id="app-container"):
            yield MoveHistory(self.game.board.size)
            yield GameBoard(self.game.board.size)
            
            yield MoveSelection()
            
        yield Footer()
            
        
    def on_mount(self):
        self.grid = self.query_one(GameGrid)
        self.move_selection = self.query_one(MoveSelection)
        self.move_history_container = self.query_one(MoveHistory)
       
        
        self.game_board_header = self.query_one(GameBoardHeader) 
        self.grid.sync(self.game.board.to_squares())
        self.grid.mark_valid_moves(self.game.legal_moves)
        self.move_selection.moves = (self.game.legal_moves)
        
        
    def update_game(self,coord:Square):
        # clear the highlighted cell and valid move hints
        self.grid.clear_highlight()
        self.grid.clear_valid_moves()
       
        # update the engine
        self.game.move(coord)
        # update the grid ui and display the valid moves
        self.grid.sync(self.game.board.to_squares())
        self.grid.mark_valid_moves(self.game.legal_moves)
        
        # update game board header
        score = self.game.score
        self.game_board_header.update(score[Player.BLACK],score[Player.WHITE],self.game.current_player)
        self.move_selection.moves = (self.game.legal_moves)
        self.move_history_container.update_history(self.game.history)
            
    ##################### Handlers #####################
        
    def on_cell_clicked(self,message:Cell.Clicked):
        self.update_game(message.coordinate)
        
        
    def on_move_selection_selected(self,message:MoveSelection.Selected):
        self.update_game(message.move)
        
        
    def on_move_selection_highlighted(self,message:MoveSelection.Highlighted):
        self.grid.clear_highlight()
        self.grid.highlight_cell(message.move)
        
        
    @on(MouseMove)
    def handle_mouse_move(self):
        if self.move_selection.highlighted_index:
            self.move_selection.highlighted_index = None
            self.grid.clear_highlight()

            

if __name__ == "__main__":
    app = Othello()
    app.run()