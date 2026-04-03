from .types import *
from .board import Board
from othellox.game import board

class Othello:
    
    def __init__(self,size:int = 8) -> None:
        self.board = Board(size)
        self.current_player = Player.BLACK
        self.winner: Player | None = None
        self.set_starting_positions()

    def set_starting_positions(self):
        '''
        Initially the board is empty, so in the beginning of the 
        game center of the board should be filled with the starting four coins.
        '''
        center = (self.board.size//2) - 1
        self.board[Coordinate(center+1,center)] = Player.WHITE
        self.board[Coordinate(center,center+1)] = Player.WHITE

        self.board[Coordinate(center,center)] = Player.BLACK
        self.board[Coordinate(center+1,center+1)] = Player.BLACK
        
    def switch_player(self):
        if self.current_player == Player.BLACK:
            self.current_player = Player.WHITE
        else:
            self.current_player = Player.BLACK
            
    @property
    def opponent_player(self) -> Player:
        return Player.WHITE if self.current_player == Player.BLACK else Player.BLACK
            
            
    def traverse_opponents(self,initial_coord:Coordinate,direction:Direction) -> list[Coordinate]:
        '''
        traverse through opponent coins concurrently in a particular
        direction until the current player coin is found
        
        - returns list of opponent coins coordinate
        '''
     
        pos = initial_coord.walk(direction)
        
        opponent_coins:list[Coordinate] = []

        # Check if next cords just after the initial_coords is opponet
        if not self.board.is_bound(pos) or self.board[pos] != self.opponent_player:
            return []

        # append the first opponet coin
        opponent_coins.append(pos)
        
        # traverse through opponents 
        
        while True:
            pos = pos.walk(direction)

            if not self.board.is_bound(pos):
                return []

            if self.board[pos] == self.opponent_player:
                opponent_coins.append(pos)
                continue
            
            # if current player coin found return
            if self.board[pos] == self.current_player:
                return opponent_coins
            
            return []
                                
    @property
    def possible_moves(self) -> list[Coordinate]:
        possible_moves = set()
        for y in range(0,self.board.size):
            for x in range(0,self.board.size):
                start = Coordinate(x,y) 
                if self.board[start] == None:# starting from empty to current player
                    for direction in Direction:
                        if (self.traverse_opponents(start,direction)):
                            possible_moves.add(start)
                            break
                        
        return list(possible_moves)
    
    def flip_coins(self,coordinate:Coordinate,player:Player):
        for direction in Direction:
            opponent_coins = self.traverse_opponents(coordinate,direction)
            for opponent_coin in opponent_coins:
                self.board[opponent_coin] = self.current_player
        
    
    def move(self,coordinate:Coordinate):
        if not (coordinate in self.possible_moves):
            return 
        # place the piece
        self.board[coordinate] = self.current_player
        # flip all coins
        self.flip_coins(coordinate,self.current_player)
        # switch players    
        self.switch_player()
        if not self.possible_moves:
            self.switch_player()