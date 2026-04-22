
from typing import Optional
from textual.binding import Binding, BindingType
from textual.events import Key
from textual.message import Message
from textual.reactive import reactive
from textual.containers import Container, Grid
from textual.widgets import Label, Static
from othellox.game.type import Square
from othellox.ui.valid_move_label import ValidMoveLabel


class MoveSelection(Container):
    
    
    DEFAULT_CSS = """
    MoveSelection{
        border:panel $secondary;
        
        
        padding-top:1;
        height:100%;
        width:19;
        border-title-align:center;
        background:$surface;
        border-title-color:$text;
    }
    
    #moves-container{
        padding-left:1;
        padding-right:1;
        grid-size: 5;
        grid-gutter: 0 0;
        grid-rows:auto;
        width:1fr;
        height:1fr;
    }
    
    #controls-label{
        border-title-color:$text;
        border-top:panel $secondary;
        border-title-align:center;
        padding-left:1;
        padding-right:1;
    
    }
    
   
    """
    
    can_focus = True
    
    BINDINGS = [
        Binding("left,a","cursor_left",priority=True,system=True,show=True),
        Binding("right,d","cursor_right",priority=True),
        Binding("up,w","cursor_up",priority=True),
        Binding("down,s","cursor_down",priority=True)
    ]
    
    highlighted_index = reactive[Optional[int]](None, init=False)
    moves = reactive[list[Square]]([],init=False)
    
    
    class Highlighted(Message):
        def __init__(self,move:Square):
            super().__init__()
            self.move = move
            
    class Selected(Message):
        def __init__(self,move:Square):
            super().__init__()
            self.move = move

    def on_mount(self):
        self.border_title = "Select Move"
        self.query_one("#controls-label").border_title = "control hint"
        self.moves_container = self.query_one("#moves-container",Grid)
        
    def compose(self):
        yield Grid(id="moves-container")
        yield Static("[dim bold]use arrow keys or wasd to nav. press enter to play move[/]",id="controls-label")
    
    
    def watch_moves(self):
        self.highlighted_index = None
        self.moves_container.remove_children()
        self.moves_container.mount_all([ValidMoveLabel(index,move) for index,move in enumerate(self.moves)])
    
    def watch_highlighted_index(self):
        legal_moves = self.query(ValidMoveLabel)        
        for legal_move in legal_moves:
            legal_move.highlight = legal_move.index == self.highlighted_index
            if legal_move.highlight:
                self.post_message(self.Highlighted(legal_move.move))

        
    def action_cursor_right(self):
        if self.highlighted_index is None:
            self.highlighted_index = 0
        else:
            self.highlighted_index = (self.highlighted_index + 1) % len(self.moves)
                
    def action_cursor_left(self):
        if self.highlighted_index is None:
            self.highlighted_index = len(self.moves) - 1
        else:
            self.highlighted_index = (self.highlighted_index - 1) % len(self.moves)

    def action_cursor_down(self):
        if self.highlighted_index is None:
            self.highlighted_index = 0
            return

        cols = 5
        n = len(self.moves)

        row = self.highlighted_index // cols
        col = self.highlighted_index % cols

        new_row = row + 1
        
        if new_row * cols >= n:
            new_row = 0

        new_index = new_row * cols + col

        if new_index >= n:
            new_index = n - 1

        self.highlighted_index = new_index


    def action_cursor_up(self):
        if self.highlighted_index is None:
            self.highlighted_index = 0
            return

        cols = 5
        n = len(self.moves)

        row = self.highlighted_index // cols
        col = self.highlighted_index % cols

        new_row = row - 1

        if new_row < 0:
            new_row = (n - 1) // cols

        new_index = new_row * cols + col

        if new_index >= n:
            new_index = n - 1

        self.highlighted_index = new_index
        
        
    def on_key(self,event:Key):
        if event.key == "enter" and self.highlighted_index!=None:
            for move_label in self.query(ValidMoveLabel):
                if move_label.index == self.highlighted_index:
                    self.post_message(self.Selected(move_label.move))
                    
    