from enum import Enum

class CellData(Enum):
    EMPTY = ""
    WHITE = "⚪"
    BLACK = "⚫"
    
    
class Shade(Enum):
    LIGHT = 0
    DARK = 1