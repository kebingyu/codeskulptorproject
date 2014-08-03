"""
Mini-max Tic-Tac-Toe Player
"""

import poc_ttt_gui
import poc_ttt_provided as provided

# Set timeout, as mini-max can take a long time
import codeskulptor
codeskulptor.set_timeout(60)

# SCORING VALUES - DO NOT MODIFY
SCORES = {provided.PLAYERX: 1,
          provided.DRAW: 0,
          provided.PLAYERO: -1}

def mm_move(board, player):
    """
    Make a move on the board.
    
    Returns a tuple with two elements.  The first element is the score
    of the given board and the second element is the desired move as a
    tuple, (row, col).
    """
    # check state    
    state = board.check_win()
    # game over, return final score
    if (state != None):
        return SCORES[state], (-1, -1)
    max_score = -1
    max_move = None
    # get all possible moves
    empty_squares = board.get_empty_squares()
    for empty_square in empty_squares:
        board_clone = board.clone()
        # attempt one possible move
        board_clone.move(empty_square[0], empty_square[1], player)
        # recursive call minmax
        result = mm_move(board_clone, provided.switch_player(player))
        # store a best move
        curr_score = SCORES[player] * result[0]
        if curr_score == 1:
            return result[0], empty_square
        if max_move == None or curr_score > SCORES[player] * max_score:
            max_score = result[0]
            max_move = empty_square
    # return best move
    return max_score, max_move

def move_wrapper(board, player, trials):
    """
    Wrapper to allow the use of the same infrastructure that was used
    for Monte Carlo Tic-Tac-Toe.
    """
    move = mm_move(board, player)
    assert move[1] != (-1, -1), "returned illegal move (-1, -1)"
    return move[1]

# Test game with the console or the GUI.
# Uncomment whichever you prefer.
# Both should be commented out when you submit for
# testing to save time.

#provided.play_game(move_wrapper, 1, False)        
poc_ttt_gui.run_gui(3, provided.PLAYERO, move_wrapper, 1, False)
