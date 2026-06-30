



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
        
        &>Label{
            width:1fr;
            height:1;
        }
        
        #heading-label{
            text-align:center;
            padding-left:2;
        }
        
        #score-label{
            text-align:right;
        }
        #current-player-label{
            text-align:left;  
        }
    }

    """
    
    score = reactive[dict[Player,int]]({Player.BLACK:2,Player.WHITE:2})
    current_player = reactive[Player](Player.BLACK,init=False,recompose=True)
    heading = reactive[str]("Othello",init=False,recompose=True)
    
    def __init__(self):
        super().__init__()
    
    def compose(self):
        yield Label(f"[bold]T:[/]{"⚫" if self.current_player == Player.BLACK else "⚪"}",id="current-player-label")
        yield Label(f"[bold dim]{self.heading}[/]",id="heading-label")
        yield Label(f"[bold]S:[/]⚫ {self.score[Player.BLACK]:02} ⚪ {self.score[Player.WHITE]:02}",id="score-label")
