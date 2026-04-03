from enum import Enum
from typing import TypeAlias

from dataclasses import dataclass



class Player(Enum):
    BLACK = 0
    WHITE = 1
    


@dataclass(frozen=True)
class Coordinate:
    x: int
    y: int

    def walk(self, direction: "Direction", steps: int = 1) -> "Coordinate":
        return Coordinate(
            self.x + direction.dx * steps,
            self.y + direction.dy * steps
        )
        
    
class Direction(Enum):
    TOP = (0, 1)
    BOTTOM = (0, -1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)
    TOP_LEFT = (-1, 1)
    TOP_RIGHT = (1, 1)
    BOTTOM_LEFT = (-1, -1)
    BOTTOM_RIGHT = (1, -1)

    @property
    def dx(self) -> int:
        return self.value[0]

    @property
    def dy(self) -> int:
        return self.value[1]


Cell:TypeAlias = Player | None