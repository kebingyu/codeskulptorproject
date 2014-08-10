"""
Solitaire Mancala
"""

class SolitaireMancala:
    def __init__(self):
        self.board = [0]
    
    def set_board(self, configuration):
        self.board = list(configuration)
        
    def __str__(self):
        result = ''
        for idx in range(len(self.board) - 1, -1, -1):
            result += str(self.board[idx]) + ', ' 
        return '[' + result.rstrip(', ') + ']'
    
    def get_num_seeds(self, house_num):
        return self.board[house_num]
    
    def is_legal_move(self, house_num):
        seeds = self.get_num_seeds(house_num)
        if 0 == seeds:
            return False
        if house_num == seeds:
            return True
        else:
            return False
        
    def apply_move(self, house_num):
        if self.is_legal_move(house_num):
            self.board[house_num] = 0
            for idx in range(0, house_num):
                self.board[idx] += 1
        else:
            return 'illegal move'
        
    def choose_move(self):
        legal_moves = []
        for idx in range(1, len(self.board)):
            if self.is_legal_move(idx):
                legal_moves.append(idx)
        if legal_moves:
            return min(legal_moves)
        else:
            return 0
        
    def is_game_won(self):
        for idx in range(1, len(self.board)):
            if self.board[idx] != 0:
                return False
        return True
    
    def plan_moves(self):
        clone = SolitaireMancala()
        clone.set_board(self.board)
        moves = []
        while not clone.is_game_won():
            curr_move = clone.choose_move()
            if curr_move != 0:
                clone.apply_move(curr_move)
                moves.append(curr_move)
            else:
                break
        return moves
    
import poc_mancala_gui
poc_mancala_gui.run_gui(SolitaireMancala())
