
from textual.app import App,ComposeResult


from othellox.game.type import Player
from othellox.ui.board.board_header import GameBoardHeader
from othellox.ui.board.grid import Grid
from othellox.ui.board.cell import Cell

from othellox.game.engine import OthelloEngine
from othellox.ui.board.game_board import GameBoard

class Othello(App):
    
    def __init__(self):
        super().__init__()
        self.game = OthelloEngine(8)


    def compose(self)->ComposeResult:
        yield GameBoard(self.game.board.size)
        
    def on_mount(self):
        self.grid = self.query_one(Grid)
        self.game_board_header = self.query_one(GameBoardHeader) 
        self.grid.sync(self.game.board.to_squares())
        self.grid.mark_valid_moves(self.game.legal_moves)
            
    ##################### Handlers #####################
        
    def on_cell_clicked(self,message:Cell.Clicked):
        coord = message.coordinate
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
        # update game board header
        score = self.game.score
        self.game_board_header.update(score[Player.BLACK],score[Player.WHITE],self.game.current_player)
            

if __name__ == "__main__":
    app = Othello()
    app.run()