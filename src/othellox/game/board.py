from .types import *

class Board:
    def __init__(self,size:int):
        self.size = size
        self.board:list[list[Cell]] =  [[None for cell in range(self.size)] for row in range(self.size)]

    def __getitem__(self, coordinate:Coordinate):
        return self.board[coordinate.y][coordinate.x]
    
    def __setitem__(self, coordinate:Coordinate, value):
        self.board[coordinate.y][coordinate.x] = value

    def __str__(self) -> str:
        ascii_board = ""
        
        #header
        ascii_board += "  ┌" + "─────┬" * (self.size - 1) + "─────┐\n"

        for i, row in enumerate(self.board[::-1]):
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
        return (0 <= coord.x < self.size) and (0 <= coord.y < self.size)
