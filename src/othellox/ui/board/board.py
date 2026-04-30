from typing import Dict, Optional
from textual import on
from textual.binding import Binding
from textual.message import Message
from textual.reactive import reactive
from textual.widget import Widget
from textual.app import ComposeResult
from othellox.game.type import Player, Square
from othellox.ui.board.header import GameBoardHeader
from othellox.ui.board.cell import Cell, CellData
from othellox.ui.board.grid import GameGrid

from textual.widgets import Button
    

class OthelloBoard(Widget):
    DEFAULT_CSS = """
    OthelloBoard{
        layout:vertical;
        background:$panel;
        width:auto;
        height:auto;
        padding-left:1;
        padding-right:1;
        border-bottom:thick transparent;
    }

    """
 
    can_focus = True
    
    BINDINGS = [
        Binding("left,a","navigate_left"),
        Binding("right,d","navigate_right"),
        Binding("enter","cell_click")
    ]
    
    highlighted_index = reactive[Optional[int]](None, init=False)
    hints = reactive[list[Square]]([],init=False)

    
    def __init__(self,grid_size):
        super().__init__()
        self.grid_size = grid_size
        
        
    def on_mount(self):
        self.header = self.query_one(GameBoardHeader)
        self.grid = self.query_one(GameGrid)
        self.disabled = True
       
    
    def compose(self)->ComposeResult:
        yield GameBoardHeader()
        yield GameGrid(self.grid_size)
        
        
    ######## events ############
        
    class CellHighlighted(Message):
        def __init__(self,highlighted_square:Square):
            super().__init__()
            self.move = highlighted_square
            
            
    class CellClicked(Message):
        def __init__(self,move:Square):
            super().__init__()
            self.move = move
        
    ########### API ###############
    
    def _find_cell(self,sqaure_to_find:Square) -> Cell:
        for square, cell in self.grid.cells.items():
            if sqaure_to_find == square:
                return cell
        raise Exception

    def diaplay_hints(self,hints:list[Square]):
        self.hints = hints
        
    def clear_hints(self):
        for cell in self.grid.cells.values():
            cell.is_hint = False
        
    def highlight(self,highlight_sqaure:Square):
        self._find_cell(highlight_sqaure).highlight = True
      
            
    def clear_highlight(self):
        for cell in self.grid.cells.values():
            cell.highlight = False
    
    def update_cells(self,squares:dict[Square,Player | None]):
        for sqaure,data in squares.items():
            match (data):
                case Player.WHITE:
                    cell_data = CellData.WHITE
                case Player.BLACK:
                    cell_data = CellData.BLACK
                case None:
                    cell_data = CellData.EMPTY
                case _:
                    raise Exception
            self._find_cell(sqaure).data = cell_data  

                
    def update_header(self,current_player:Optional[Player] = None,score:Optional[Dict[Player,int]] = None ,heading:Optional[str] = None):
        if current_player!=None:
            self.header.current_player = current_player
            
        if score !=None:
            self.header.score  = score
            
        if heading != None:
            
            self.header.heading = heading
        
        
    ######## internal state ###################3
        
    def watch_hints(self):
        for sqaure, cell in self.grid.cells.items():
            cell.is_hint = sqaure in self.hints        
            
    def watch_highlighted_index(self):
        if self.highlighted_index!=None:
            highlighted_square = self.hints[self.highlighted_index]
            self.post_message(self.CellHighlighted(highlighted_square))
            
            
    ####### binding actions ############
    
    def action_navigate_right(self):
        if self.hints:
            if self.highlighted_index is None:
                self.highlighted_index = 0
            else:
                self.highlighted_index = (self.highlighted_index + 1) % len(self.hints)
                
    def action_navigate_left(self):
        if self.hints:
            if self.highlighted_index is None:
                self.highlighted_index = 0
            else:
                self.highlighted_index = (self.highlighted_index - 1) % len(self.hints)
            
    def action_cell_click(self):
        
        if self.highlighted_index != None:
            self.post_message(self.CellClicked(self.hints[self.highlighted_index]))
            
        
    @on(Cell.Clicked)    
    def handle_cell_click(self,event:Cell.Clicked):
        self.post_message(self.CellClicked(event.coordinate))