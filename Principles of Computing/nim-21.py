"""
A simple Monte Carlo solver for Nim
http://en.wikipedia.org/wiki/Nim#The_21_game
"""

import random
import codeskulptor
codeskulptor.set_timeout(20)

MAX_REMOVE = 3
TRIALS = 10000

def evaluate_position(num_items):
    """
    Monte Carlo evalation method for Nim
    """
    results = []
    max_ratio = 0.0
    for init_move in range(MAX_REMOVE, 0, -1):
        count_win = 0
        curr_items = num_items - init_move
        # best move found
        if curr_items <= 0:
            return init_move
        # else, use Monte Carlo
        for _ in range(TRIALS):
            curr_items = num_items - init_move
            count_step = 0 # determine who is the current player
            while curr_items > 0:
                curr_items -= random.randrange(1, MAX_REMOVE + 1)
                count_step += 1
            # game over, check status
            if count_step % 2 == 0: # computer win
                count_win += 1
        # trial runs over, get win ratio
        win_ratio = count_win / float(TRIALS)
        if win_ratio > max_ratio:
            best_move = init_move
            max_ratio = win_ratio
    return best_move

def play_game(start_items):
    """
    Play game of Nim against Monte Carlo bot
    """
    
    current_items = start_items
    print "Starting game with value", current_items
    while True:
        comp_move = evaluate_position(current_items)
        current_items -= comp_move
        print "Computer choose", comp_move, ", current value is", current_items
        if current_items <= 0:
            print "Computer wins"
            break
        player_move = int(input("Enter your current move"))
        current_items -= player_move
        print "Player choose", player_move, ", current value is", current_items
        if current_items <= 0:
            print "Player wins"
            break

#play_game(5)
print evaluate_position(10)
