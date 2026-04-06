from othellox.game.engine import Othello
from othellox.game.type import Coordinate

def run():
    game = Othello(8)
    
 
    i = 0 
    while i<10:
        print(game.current_player)
        print(game.state)
        print(game.board.ascii)
        print(game.available_moves)
        
        x = int(input("Enter x : "))
        y = int(input("Enter y : "))
        
        
        game.move(Coordinate(x,y))
        
        i+= 1
        
        
    
    
if __name__=="__main___":
    run()