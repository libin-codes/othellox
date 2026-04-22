from textual.app import ComposeResult
from textual.containers import Grid
from textual.widget import Widget
from textual.widgets import Label

from othellox.game.type import Square


class MoveHistory(Widget):
    DEFAULT_CSS = """
    MoveHistory {
        border: panel $secondary;
        padding-left: 1;
        padding-right: 1;
        padding-top: 1;
        height: 100%;
        width: 21;
        border-title-align: center;
        border-title-color:$text;
        background: $surface;
    }

    MoveHistory #history-grid {
        grid-size: 3;
        grid-gutter: 0 1;
        height: auto;
    }

    MoveHistory .move-cell {
        width: 1fr;
        height: 1;
    }
    """

    def __init__(self, grid_size: int) -> None:
        super().__init__()
        self.total_moves = (grid_size * grid_size) - 4
        self.history_grid_cols = 3

    def compose(self) -> ComposeResult:
      
        rows = (self.total_moves + self.history_grid_cols - 1) // self.history_grid_cols
        with Grid(id="history-grid"):
            for r in range(rows):
                for c in range(self.history_grid_cols):
                    index = c * rows + r + 1
                    yield Label(
                        f"[dim]{index:02} [/]──",
                        id=f"move-{index}",
                        classes="move-cell",
                    )
                 
    def on_mount(self) -> None:
        self.border_title = "Move History"

    def update_history(self, history: list[Square]) -> None:    
        for index,move in enumerate(history):
            cell = self.query_one(f"#move-{index+1}", Label)
            cell.update(f"[dim]{index+1:02} [/][bold $accent]{move}[/]")
           