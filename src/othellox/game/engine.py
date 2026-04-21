'''Core Othello game engine implementation.

This module implements the primary Othello game logic, including:
- Board initialization with starting positions
- Move validation and execution
- Piece flipping mechanics
- Game state management and win condition detection

The Othello game follows standard rules where players alternate placing pieces
and capturing opponent pieces by flanking them with their own pieces.
'''  

from .board import Board
from .type import Square, Player,Index,GameResult,GameState,Direction
from .error import InvalidMoveError,GameOverError,InvalidBoardSizeError
from typing import Dict
    
class OthelloEngine:
    def __init__(self, size: int = 8) -> None:
        
        """Initialize a new Othello game.
        
        Args:
            size: The board size - side length of the square board (default: 8 ,minimum:6, maximum:20).
                  Set up standard Othello with the starting configuration.
        """
        if not (6 <= size <= 26):
            raise InvalidBoardSizeError("size must be between 6 and 20")
        if size % 2 != 0:
            raise InvalidBoardSizeError("size must be even")
        self.board = Board(size)
        self._history:list[Square] = []
        self._current_player = Player.BLACK
        self._state = GameState(None)
        self._set_starting_positions()

    def _set_starting_positions(self) -> None:
        """Set up the standard starting position.
        
        Positions 4 pieces in the center of the board:
        - Black pieces at (center, center) and (center+1, center+1)
        - White pieces at (center+1, center) and (center, center+1)
        
        This follows standard Othello rules for an 8x8 board.
        """
        center = (self.board.size//2) - 1
        self.board._set(Index(center+1,center), Player.BLACK)
        self.board._set(Index(center,center+1), Player.BLACK)

        self.board._set(Index(center,center),Player.WHITE)
        self.board._set(Index(center+1,center+1), Player.WHITE)
        
    @property
    def current_player(self) -> Player:
        return self._current_player
    
    @property
    def history(self) -> list[Square]:
        return self._history
        
    @property
    def opponent_player(self) -> Player:
        """Get the opponent of the current player.
        
        Returns:
            The Player enum for the opponent.
        """
        return Player.WHITE if self.current_player == Player.BLACK else Player.BLACK
    
    @property
    def score(self) -> Dict[Player, int]:
        """Get the current score for both players.
        
        Returns:
            A dictionary mapping Player enum values to their piece count.
        """
        white_score = 0
        black_score = 0
        
        for cell in self.board.to_squares().values():
            match cell:
                case Player.WHITE:
                    white_score += 1
                    
                case Player.BLACK:
                    black_score += 1
                        
        return {
            Player.WHITE: white_score,
            Player.BLACK: black_score
        }
        
    @property
    def legal_moves(self) -> list[Square]:
        """Get all valid moves for the current player.
        
        A valid move is an empty sqaure where placing a piece would outflank
        at least one opponent piece in any direction.
        
        Returns:
            A list of Sqaure representing valid moves.
            where Sqaure -> Algebraic notation. ex: "a1", "b2", "h3", etc
        """
        possible_moves = set()
        for y in range(self.board.size):
            for x in range(self.board.size):
                start = Index(x, y) 
                if self.board[start] is None and self._outflank(start):
                    possible_moves.add(start)
                    
        possible_moves = [self._index_to_sqaure(move) for move in possible_moves]
        possible_moves.sort()
        return possible_moves
    
    @property 
    def state(self) -> GameState:
        """Get the current game state.
        
        Returns:
            The current GameState containing result info and game status.
        """
        return self._state
        
    def _switch_player(self) -> None:
        """Switch the current player to the opponent."""
        self._current_player = self.opponent_player
            
    def _outflank(self, start: Index) -> list[Index]:
        """Find all opponent pieces that would be outflanked by placing at start.
        
        Traverses in all 8 directions from the start position, collecting opponent
        pieces until either a current player piece (outflank confirmed), board edge
        (no outflank), or empty cell (no outflank) is reached.
        
        Args:
            start: The Index of the potential placement location.
            
        Returns:
            A list of opponent piece Indexs that would be flipped by this move.
                Returns empty list if no outflanking occurs.
        """
        opponent_coins: list[Index] = []
        for direction in Direction:
            path: list[Index] = []
            pos = start.walk(direction)        
            # traverse through opponents 
            while (self.board.is_bound(pos) and self.board[pos] == self.opponent_player):
                path.append(pos)
                pos = pos.walk(direction)
            
            if path and self.board.is_bound(pos) and self.board[pos] == self.current_player:
                opponent_coins.extend(path)
        return opponent_coins
                                

    
    def _flip_coins(self, index: Index) -> None:
        """Flip (convert) all opponent pieces outflanked by a move.
        
        Args:
            coordinate: The Index where the current player placed a piece.
        """
        for opponent_coin in self._outflank(index):
            self.board._set(opponent_coin,self.current_player)
    
    def _index_to_sqaure(self,coord: Index) -> Square:

        return f"{chr(coord.x + ord('a'))}{coord.y + 1}"
    
    def _sqaure_to_index(self,sqaure:Square) -> Index:
        x = ord(sqaure[0]) - ord('a')
        y = int(sqaure[1]) - 1
        return Index(x,y)

            
    def move(self, sqaure: Square) -> None:
        """Execute a move for the current player.
        
        Places a piece at the given coordinate, flips all outflanked opponent pieces,
        switches to the opponent, and checks for end-game conditions.
        
        Args:
            sqaure : represents algebraic notation, ex: "a1", "e3, "h3", etc
            
        Raises:
            InvalidMoveError: If the coordinate is not a valid move for the current player.
            GameOverError: If the game has already ended.
        """ 
        
        if self._state.is_over:
            raise GameOverError()
        
        if sqaure not in self.legal_moves:
            raise InvalidMoveError(sqaure)
        
        self._history.append(sqaure)
        
        index = self._sqaure_to_index(sqaure)
        
        # place the piece
        self.board._set(index,self.current_player)
        # flip opponent coins
        self._flip_coins(index)
        # switch players    
        self._switch_player()
        # check if opponent can move
        if not self.legal_moves:
            self._switch_player()
            # check if both players have no moves -> game over
            if not self.legal_moves:
                score = self.score
                if score[Player.WHITE] > score[Player.BLACK]:
                    result = GameResult.WHITE_WINS
                elif score[Player.BLACK] > score[Player.WHITE]:
                    result = GameResult.BLACK_WINS
                else:
                    result = GameResult.DRAW
                self._state = GameState(result)
                
                
    def copy(self) -> "OthelloEngine":
        new_game = OthelloEngine(self.board.size)
        new_game._current_player = self.current_player
        new_game._state = self._state
        
        for y in range(self.board.size):
            for x in range(self.board.size):
                coord = Index(x, y)
                new_game.board._set(coord, self.board[coord])
                
        return new_game