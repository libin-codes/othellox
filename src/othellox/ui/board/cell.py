from enum import Enum
from textual.events import Click
from textual.message import Message
from textual.widget import Widget
from textual.widgets import Static
from textual.reactive import reactive
from othellox.game.type import Coordinate
from textual.color import Color

class CellData(Enum):
    EMPTY = ""
    WHITE = "⚪"
    BLACK = "⚫"
    
    
class Shade(Enum):
    LIGHT = 0
    DARK = 1
    
    
class Cell(Widget):
    DEFAULT_CSS = """
    Cell{
        height:3;
        width:7 ;
        content-align-horizontal: center;
        content-align-vertical: middle;
        &:hover{
            opacity:94%;
        }
    }
    """
    
    class Clicked(Message):
        
        def __init__(self,coordinate:Coordinate) -> None:
            self.coordinate = coordinate
            super().__init__()
    
    data = reactive(CellData.EMPTY)
    is_valid_move = reactive(False)
    
    def __init__(self,coordinate:Coordinate,background_shade:Shade,color:Color = Color.parse("green")):
        """
        Args:
            coordinate (Coordinate): cell coordinate
            background_shade (Shade): 0 or 1 , 0 -> light, 1 -> dark
        """
        super().__init__()
        
        self.coordinate = coordinate
        self.shade = background_shade
        self.color = color
        
    def on_mount(self):
        self.styles.background = self.color.darken(0.02) if self.shade == Shade.DARK else self.color
       
        
        
    def render(self):
        if not self.is_valid_move:
            return self.data.value
        return "●"
    
    
    def on_click(self,event:Click):
        if self.is_valid_move:
            self.app.post_message(self.Clicked(self.coordinate))