"""Board management for the Othello game.

This module handles the 2D game board, cell access, and board visualization.
It provides a clean interface for placing pieces and rendering the board state.
"""

from .type import Coordinate,Cell,Player

class Board:
    """Manages the Othello game board.
    
    The board is a square grid (typically 8x8) where pieces (players) are placed.
    It provides indexing via Coordinate objects and ASCII visualization.
    
    Attributes:
        size: The dimensions of the square board (size x size).
    """
    def __init__(self, size: int) -> None:
        """Initialize the board with given dimensions.
        
        Args:
            size: The side length of the square board (default: 8).
        """
        self.size = size
        self._board: list[list[Cell]] = [[None for cell in range(self.size)] for row in range(self.size)]
        
    

    def __getitem__(self, coordinate: Coordinate) -> Cell:
        """Get the cell value at a given coordinate.
        
        Args:
            coordinate: The Coordinate of the cell to access.
            
        Returns:
            The cell value (Player or None).
        """
        return self._board[coordinate.y][coordinate.x]
    
    def _set(self, coordinate: Coordinate, value:Player | None):
        self._board[coordinate.y][coordinate.x] = value
        
        
    @property
    def grid(self) -> list[list[Cell]]:
        """Get a read-only copy of the board grid.
        
        Returns:
            A deep copy of the internal board representation.
        """
        return [row[:] for row in self._board]

    @property
    def ascii(self) -> str:
        """Generate an ASCII representation of the board for display.
        
        Returns:
            A string containing a formatted ASCII board with coordinates and pieces.
            Uses ⚫ for black pieces, ⚪ for white pieces, and spaces for empty cells.
        """
        ascii_board = ""
        
        #header
        ascii_board += "  ┌" + "─────┬" * (self.size - 1) + "─────┐\n"

        for i, row in enumerate(self._board[::-1]):
            # y - axis
            ascii_board += f"{(self.size - i)-1} │"
            # board
            for cell in row:
                match cell:
                    case None:
                        content = "     "
                    case Player.BLACK:
                        content = " ⚫  "
                    case Player.WHITE:
                        content = " ⚪  "
                ascii_board += content + "│"
            ascii_board += "\n"
            if  i != self.size - 1:
                ascii_board += "  ├" + "─────┼" * (self.size - 1) + "─────┤\n"
            else:
            # footer
                ascii_board += "  └" + f"─────┴" * (self.size - 1) + "─────┘\n"
            
        # x - axis
        ascii_board += "   "
        for x in range(self.size): ascii_board += f"{x:^5} "
        return ascii_board
    
    def is_bound(self, coord: Coordinate) -> bool:
        """Check if a coordinate is within board boundaries.
        
        Args:
            coord: The Coordinate to check.
            
        Returns:
            True if the coordinate is within the board, False otherwise.
        """
        return (0 <= coord.x < self.size) and (0 <= coord.y < self.size)
