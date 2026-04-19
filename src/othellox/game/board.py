"""Board management for the Othello game.

This module handles the 2D game board, cell access, and board visualization.
It provides a clean interface for placing pieces and rendering the board state.
"""
from .type import Index,Player

class Board:
    """Manages the Othello game board.
    
    The board is a square grid (typically 8x8) where pieces (players) are placed.
    It provides indexing via Index objects and ASCII visualization.
    
    Attributes:
        size: The dimensions of the square board (size x size).
    """
    def __init__(self, size: int) -> None:
        """Initialize the board with given dimensions.
        
        Args:
            size: The side length of the square board (default: 8).
        """
        self.size = size
        self._board: list[list[Player | None]] = [[None for cell in range(self.size)] for row in range(self.size)]
        
    

    def __getitem__(self, index: Index) -> Player | None:
        """Get the cell value at a given coordinate.
        
        Args:
            index: The Index of the cell to access.
            
        Returns:
            The cell value (Player or None).
        """
        return self._board[index.y][index.x]
    
    def _set(self, coordinate: Index, value:Player | None):
        self._board[coordinate.y][coordinate.x] = value
    
   
    def to_squares(self) -> dict[str, Player | None]:
        """data in each sqaure

        Returns:
            dict[str,BoardCell]: maps each sqaure to its data (Player | None)
        """
        
        y_coordinates = range(self.size,0,-1)
        x_coordinates = [chr(ord("a") + i) for i in range(self.size)]
        
        squares = {}
        
        for y,row in zip(y_coordinates,self._board[::-1]):
            for x,data in zip(x_coordinates,row):
                squares[f"{x}{y}"] = data
                
        return squares
        
        ...

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

        for y, row in zip(range(self.size,0,-1),self._board[::-1]):
            # y - axis
            ascii_board += f"{y} │"
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
            if  y != 1:
                ascii_board += "  ├" + "─────┼" * (self.size - 1) + "─────┤\n"
            else:
            # footer
                ascii_board += "  └" + f"─────┴" * (self.size - 1) + "─────┘\n"
            
        # x - axis
        ascii_board += "   "
        x_coordinates = [chr(ord("a") + i) for i in range(self.size)]
        for x in x_coordinates: ascii_board += f"{x:^5} "
        return ascii_board
    
    def is_bound(self, coord: Index) -> bool:
        """Check if a coordinate is within board boundaries.
        
        Args:
            coord: The Index to check.
            
        Returns:
            True if the coordinate is within the board, False otherwise.
        """
        return (0 <= coord.x < self.size) and (0 <= coord.y < self.size)
