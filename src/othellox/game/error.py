"""Custom exception classes for the Othello game engine.

This module defines all custom exceptions used by the Othello game.
These exceptions provide meaningful error messages and allow for
specific exception handling in client code.
"""


class OthelloError(Exception):
    """Base class for all Othello-related errors.
    
    This is the parent exception for all game-specific errors.
    Catch this exception to handle any Othello game error.
    """
    pass


class InvalidMoveError(OthelloError):
    """Raised when a move is not valid."""
    
    def __init__(self, coordinate):
        self.coordinate = coordinate
        super().__init__(f"Invalid move at {coordinate}")
        

class InvalidBoardSizeError(OthelloError):
    """Raised when the board size is not valid."""
    pass
        
        
class GameOverError(OthelloError):
    """Raised when trying to play after the game has ended."""
    
    def __init__(self):
        super().__init__("The game is already over.")