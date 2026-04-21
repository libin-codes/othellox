



from textual.reactive import reactive
from textual.containers import Container
from textual.widgets import Label

from othellox.game.type import Player


class GameBoardHeader(Container):
    
    DEFAULT_CSS = """
    GameBoardHeader{
        width:100%;
        height:auto;
        layout:horizontal; 
        background:grey;
        color:black;      
    
    }
    
    #current-player-label{
        width:1fr;
        
        
    }
    
    #black-pts-label{
        margin-right:1;
    }
    
    #score-container{
        layout:horizontal;
        width:auto;
        height:auto;
    }
 
    
    """
    
    black_pts = reactive(2,init=False,recompose=True)
    white_pts = reactive(2,init=False,recompose=True)
    current_player = reactive(Player.BLACK,init=False,recompose=True)
    
    def __init__(self):
        super().__init__()
    
    def compose(self):
        
        yield Label(f"{"⚫" if self.current_player == Player.BLACK else "⚪"} 's Turn",id="current-player-label")
        with Container(id="score-container"):
            yield Label("Score : ")
            yield Label(f"⚫ {self.black_pts:02}",id="black-pts-label")
            yield Label(f"⚪ {self.white_pts:02}",id="white-pts-label")


    def update(self,black_pts:int,white_pts:int,current_player:Player):
        self.black_pts = black_pts
        self.white_pts = white_pts
        self.current_player = current_player