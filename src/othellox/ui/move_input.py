
from textual.containers import Container
from textual.message import Message
from textual.reactive import reactive
from textual.widget import Widget
from textual.widgets import Input, Label
from textual.validation import ValidationResult, Validator
from othellox.game.type import Square



class LegalMove(Validator):
    
    def __init__(self,legal_moves) -> None:
        self.legal_moves = legal_moves
        super().__init__()
        
    def validate(self, value: str) -> ValidationResult:
        """Check a string is equal to its reverse."""
        if self.is_valid_move(value):
            return self.success()
        else:
            return self.failure("That's not a valid move :/")
    

    def is_valid_move(self,move:Square):
        return move in self.legal_moves
    

class MoveInput(Widget):
    
    DEFAULT_CSS = """
    MoveInput{
        height:auto;
        layout:horizontal;
        border:panel grey;
        border-title-align:center;
        padding-top:1;
        padding-left:2;
        padding-right:2;
        padding-bottom:0;
        background:$surface;
        background-tint: $foreground 5%;
        
        
        &>Input{
            background-tint:transparent;
        }
    
    }
    
    
    """
    
    class Submitted(Message):
        
        def __init__(self,move:Square) -> None:
            self.move = move
            super().__init__()
    
    legal_moves = reactive([])
    
    def __init__(self):
        super().__init__()
        
        
    def compose(self):

        yield Input(

            max_length=3,
            valid_empty=True,
            compact=True,
            id="move-input"
        )
  
            
        
    
    
    def on_mount(self):
        self.border_title = "Enter Move"
        self.input = self.query_one(Input)
        self.input.validators = [LegalMove(self.legal_moves)]
       
    def watch_legal_moves(self):
        self.input.validators = [LegalMove(self.legal_moves)]
      
     
        

    
    def on_input_submitted(self,event:Input.Submitted):
        if (event.validation_result!=None and event.validation_result.is_valid):
            self.input.clear()
            self.app.post_message(self.Submitted(event.value))
    
        
