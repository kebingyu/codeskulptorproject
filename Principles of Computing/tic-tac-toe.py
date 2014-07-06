"""
Monte Carlo Tic-Tac-Toe Player
"""

import random
import poc_ttt_gui
import poc_ttt_provided as provided

# Constants for Monte Carlo simulator
# Change as desired
NTRIALS = 100    # Number of trials to run
MCMATCH = 1.0  # Score for squares played by the machine player
MCOTHER = 1.0  # Score for squares played by the other player

# Constants for board
EMPTY = provided.EMPTY
PLAYERX = provided.PLAYERX
PLAYERO = provided.PLAYERO
DRAW = provided.DRAW
    
# Add your functions here.
def mc_trial(board, player):
    """
    This function takes a current board and the next player to move.
    And then plays a random game until the game is finished.
    """
    curr_player = player
    while board.check_win() == None:
        position = get_random_square(board.get_empty_squares())
        if position:
            board.move(position[0], position[1], curr_player)
            curr_player = provided.switch_player(curr_player)
        else:
            break
    return

def mc_update_scores(scores, board, player):
    """
    This function takes a grid of scores (a list of lists) with the 
    same dimensions as the Tic-Tac-Toe board, a board from a completed 
    game, and which player the machine player is.
    """
    dim = board.get_dim()
    result = board.check_win()
    if result in (PLAYERX, PLAYERO):
        if result == player:
            factor = 1
        else:
            factor = -1
        for idx_i in range(dim):
            for idx_j in range(dim):
                status = board.square(idx_i, idx_j)
                if (status == EMPTY):
                    scores[idx_i][idx_j] += 0.0
                elif (status == player):
                    scores[idx_i][idx_j] += MCMATCH * factor
                elif (status != player):
                    scores[idx_i][idx_j] += -MCOTHER * factor

def get_best_move(board, scores):
    """
    This function takes a current board and a grid of scores.
    """
    empty_squares = board.get_empty_squares()
    if empty_squares:
        max_score = float('-inf')
        max_score_positions = []
        # get list of empty squares with max score
        for position in empty_squares:
            square_score = scores[position[0]][position[1]]
            if not max_score_positions:
                max_score = square_score
                max_score_positions.append(position)
            elif square_score == max_score:
                max_score_positions.append(position)
            elif square_score > max_score:
                max_score = square_score
                max_score_positions = [position]
        # randomly choose a square
        return get_random_square(max_score_positions)        
    else:
        return None
            
def mc_move(board, player, trials):
    """
    This function takes a current board, which player the machine 
    player is, and the number of trials to run.
    """
    dim = board.get_dim()
    scores = [[0 for _ in range(dim)] for _ in range(dim)]
    for _ in range(trials):
        board_clone = board.clone()
        mc_trial(board_clone, player)
        mc_update_scores(scores, board_clone, player)
    return get_best_move(board, scores)

def get_random_square(squares):
    """
    Pick a random square from the given squares list.
    This funciton either returns a tuple or None.
    """
    if squares:
        return squares[random.randrange(len(squares))]
    else:
        return None

# Test game with the console or the GUI.
# Uncomment whichever you prefer.
# Both should be commented out when you submit for
# testing to save time.

#provided.play_game(mc_move, NTRIALS, False)        
#poc_ttt_gui.run_gui(3, provided.PLAYERX, mc_move, NTRIALS, False)
