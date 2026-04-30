from textual import on
from textual.app import App,ComposeResult
from textual.widgets import Footer
from othellox.game.type import Square
from othellox.game.engine import OthelloEngine
from othellox.ui.board.board import OthelloBoard

class Othello(App):
    
    DEFAULT_CSS = """
    Screen{
        width:100%;
        height:100%;
        align:center middle;
        background:$background;
        hatch: left green 10%;
        
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
        yield OthelloBoard(self.game.board.size)
        yield Footer()
            
        
    def on_mount(self):
        self.game_board = self.query_one(OthelloBoard)
        self.game_board.update_cells(self.game.board.to_squares())
        self.game_board.diaplay_hints(self.game.legal_moves)
        
        
    def update_game(self,coord:Square):
        # update the engine
        self.game.move(coord)
        # clear the previous highlighted cell and valid move hints
        self.game_board.clear_highlight()
        self.game_board.clear_hints()
        # update the grid ui and display the current valid moves
        self.game_board.update_cells(self.game.board.to_squares())
        self.game_board.diaplay_hints(self.game.legal_moves)
        self.game_board.update_header(self.game.current_player,self.game.score)
      
    ##################### Handlers #####################
        
    @on(OthelloBoard.CellHighlighted)
    def handle_cell_highlighted(self,message:OthelloBoard.CellHighlighted):
        self.game_board.clear_highlight()
        self.game_board.highlight(message.move)
        
    
    @on(OthelloBoard.CellClicked)
    def handle_cell_clicked(self,message:OthelloBoard.CellClicked):
        self.update_game(message.move)
        self.game_board.highlighted_index = None
        
if __name__ == "__main__":
    app = Othello()
    app.run()