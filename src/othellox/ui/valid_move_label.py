from textual.reactive import reactive
from textual.widgets import Label


class ValidMoveLabel(Label):
    
    DEFAULT_CSS = """
    ValidMoveLabel{
        &.-highlight{
            background:$accent;
            text-style:bold;
            color:$text;
        }
    }
    """
    
    
    highlight = reactive(False)

    def __init__(self,index:int,move:str):
        super().__init__()
        self.index = index
        self.move = move
        
    def render(self):
        return self.move
        
    def watch_highlight(self):
        
        self.set_class(self.highlight,"-highlight")
     
            
    