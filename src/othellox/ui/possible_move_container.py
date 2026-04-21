

from textual.containers import Container
from textual.widgets import Label

from othellox.game.type import Square


class PossibleMoves(Label):
    
    
    DEFAULT_CSS = """
    PossibleMoves{
        border:panel grey;
        padding-left:1;
        padding-right:1;
        padding-top:1;
        height:1fr;
        width:18;
        border-title-align:center;
        background:$surface;
        
    }
    
    """
    
    
    def on_mount(self):
        self.border_title = "Legal Moves"
    
    def update_possible_moves(self,possible_moves:list[Square]):
        self.update(" ".join(possible_moves))
    