
from textual import on
from textual.app import App,ComposeResult
from textual.widgets import Footer, Header
from othellox.game.type import Player, Square
from othellox.game.engine import OthelloEngine
from othellox.ui.board.board import OthelloBoard

class Othello(App):
    
    DEFAULT_CSS = """
    Screen{
        align:center middle;
        background:$background;
        hatch: left green 10%;
        
    }
   
    """
    
    
    def __init__(self):
        super().__init__()
        self.game = OthelloEngine(12)


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
        # clear the previous highlighted cell and legal move hints
        self.game_board.clear_highlight()
        self.game_board.clear_hints()
        # update cell content and display the current legal moves
        self.game_board.update_cells(self.game.board.to_squares())
        self.game_board.diaplay_hints(self.game.legal_moves)
        #update header
        game_state = self.game.state
        if game_state.is_over:
            if game_state.is_draw:
                heading = "DRAW"
            else:
                winner = "⚫" if game_state == Player.BLACK else "⚪"
                heading = f"{winner} WON"
    
            self.game_board.update_header(heading=heading)
        else:
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