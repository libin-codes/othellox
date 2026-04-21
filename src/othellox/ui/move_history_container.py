from ctypes.wintypes import LANGID

from textual.containers import Container
from textual.widgets import Label

from othellox.game.type import Square


class MoveHistory(Label):

    DEFAULT_CSS = """
    MoveHistory{
        border:panel grey;
        padding-left:1;
        padding-right:1;
        padding-top:1;
        height:100%;
        width:21;
        border-title-align:center;
        background:$surface;

    }
    

    """
    
    def __init__(self,grid_size):
        super().__init__()
        self.total_moves = (grid_size*grid_size)-4
        
        
    def on_mount(self):
        self.border_title = "Move History"
        empty_history = [f"[ dim]{i:02} [/]--" for i in range(1,self.total_moves+1)]
        self.update(" ".join(empty_history))
        
        
    def update_history(self,history:list[Square]):
        history_string = [f"[ dim]{(index+1):02} [/][bold]{move}[/]" for index,move in enumerate(history[:-1])]
        last_move =  [f"[ dim]{(history.index(history[-1])+1):02} [/][white on grey]{history[-1]}[/]"]
        empty_history_string = [f"[ dim]{i:02} [/]--" for i in range(len(history)+1,self.total_moves+1)]
        self.update(" ".join(history_string + last_move +empty_history_string ))
        