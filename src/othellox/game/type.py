"""Core types and enumerations for the Othello game engine.

This module defines fundamental data structures used throughout the Othello game,
including player representations, board coordinates, directional movements, and game state.

Types:
    Player: Enumeration for game players (BLACK, WHITE).
    Coordinate: Immutable coordinate representation for board positions.
    Direction: Enumeration for eight directional movements on the board.
    GameResult: Enumeration for possible game outcomes.
    GameState: Frozen dataclass representing the current game state.
    BoardCell: Type alias for board Boardcells (Player or None).
"""

from enum import Enum
from typing import TypeAlias
from dataclasses import dataclass



class Player(Enum):
    """Enumeration representing the two players in Othello.
    
    Attributes:
        BLACK: The black player (typically moves first).
        WHITE: The white player.
    """
    BLACK = 0
    WHITE = 1
    


@dataclass(frozen=True)
class Coordinate:
    """Immutable coordinate representation for board positions.
    
    Attributes:
        x: The x-coordinate (column), 0-indexed from left.
        y: The y-coordinate (row), 0-indexed from bottom.
    """
    x: int
    y: int

    def walk(self, direction: "Direction", steps: int = 1) -> "Coordinate":
        """Move in a given direction by a specified number of steps.
        
        Args:
            direction: The Direction enum value to move towards.
            steps: Number of steps to move (default: 1).
            
        Returns:
            A new Coordinate representing the destination position.
        """
        return Coordinate(
            self.x + direction.dx * steps,
            self.y + direction.dy * steps
        )
        
    
class Direction(Enum):
    """Enumeration for the eight cardinal and diagonal directions on a board.
    
    Each direction is represented as a tuple (dx, dy) for movement calculations.
    
    Attributes:
        TOP: Upward direction (0, 1).
        BOTTOM: Downward direction (0, -1).
        LEFT: Leftward direction (-1, 0).
        RIGHT: Rightward direction (1, 0).
        TOP_LEFT: Diagonal up-left direction (-1, 1).
        TOP_RIGHT: Diagonal up-right direction (1, 1).
        BOTTOM_LEFT: Diagonal down-left direction (-1, -1).
        BOTTOM_RIGHT: Diagonal down-right direction (1, -1).
    """
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
        """The x-component of the direction vector."""
        return self.value[0]

    @property
    def dy(self) -> int:
        """The y-component of the direction vector."""
        return self.value[1]

class GameResult(Enum):
    """Enumeration for possible game outcomes.
    
    Attributes:
        BLACK_WINS: Black player wins the game.
        WHITE_WINS: White player wins the game.
        DRAW: The game ends in a draw (equal scores).
    """
    BLACK_WINS = 0
    WHITE_WINS = 1
    DRAW       = 2

BoardCell:TypeAlias = Player | None

@dataclass(frozen=True)
class GameState:
    """Immutable representation of the game state.
    
    Attributes:
        result: The GameResult if the game is over, None if the game is ongoing.
    """
    _result: GameResult | None  

    @property
    def is_over(self) -> bool:
        """Check if the game has ended.
        
        Returns:
            True if the game is over, False otherwise.
        """
        return self._result is not None

    @property
    def winner(self) -> Player | None:
        """Get the winning player, if applicable.
        
        Returns:
            The winning Player (BLACK or WHITE), or None if the game is not over or is a draw.
        """
        if self._result == GameResult.BLACK_WINS:
            return Player.BLACK
        if self._result == GameResult.WHITE_WINS:
            return Player.WHITE
        return None
    
    @property
    def is_draw(self) -> bool:
        """Check if the game ended in a draw.
        
        Returns:
            True if the game is over and is a draw, False otherwise.
        """
        return self._result == GameResult.DRAW