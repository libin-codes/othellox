
from textual.app import App,ComposeResult
from textual.containers import Container
from textual.widgets import Input


from othellox.game.type import Player, Square
from othellox.ui.board.board_header import GameBoardHeader
from othellox.ui.board.grid import Grid
from othellox.ui.board.cell import Cell

from othellox.game.engine import OthelloEngine
from othellox.ui.board.game_board import GameBoard
from othellox.ui.move_history_container import MoveHistory
from othellox.ui.move_input import MoveInput
from othellox.ui.possible_move_container import PossibleMoves

class Othello(App):
    
    DEFAULT_CSS = """
    Screen{
        width:100%;
        height:100%;
        align:center middle;
        background:green;
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
            with Container(id="side-panel"):
                yield PossibleMoves()
                yield MoveInput()
        
    def on_mount(self):
        self.grid = self.query_one(Grid)
        self.possible_moves_container = self.query_one(PossibleMoves)
        self.move_history_container = self.query_one(MoveHistory)
        self.move_input = self.query_one(MoveInput)
        self.move_input.legal_moves = self.game.legal_moves
        self.game_board_header = self.query_one(GameBoardHeader) 
        self.grid.sync(self.game.board.to_squares())
        self.grid.mark_valid_moves(self.game.legal_moves)
        self.possible_moves_container.update_possible_moves(self.game.legal_moves)
        
        
    def update_game(self,coord:Square):
        # clear the highlighted cell and valid move hints
        self.grid.clear_highlight()
        self.grid.clear_valid_moves()
        # highlight the user click
        self.grid.highlight_cell(coord)
        # update the engine
        self.game.move(coord)
        # update the grid ui and display the valid moves
        self.grid.sync(self.game.board.to_squares())
        self.grid.mark_valid_moves(self.game.legal_moves)
        self.move_input.legal_moves = self.game.legal_moves
        # update game board header
        score = self.game.score
        self.game_board_header.update(score[Player.BLACK],score[Player.WHITE],self.game.current_player)
        self.possible_moves_container.update_possible_moves(self.game.legal_moves)
        self.move_history_container.update_history(self.game.history)
            
    ##################### Handlers #####################
        
    def on_cell_clicked(self,message:Cell.Clicked):
        self.update_game(message.coordinate)
        
        
    def on_move_input_submitted(self,message:MoveInput.Submitted):
        self.update_game(message.move)

            

if __name__ == "__main__":
    app = Othello()
    app.run()