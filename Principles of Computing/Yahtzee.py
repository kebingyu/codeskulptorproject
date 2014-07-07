"""
Planner for Yahtzee
Simplifications:  only allow discard and roll, only score against upper level
"""

# Used to increase the timeout, if necessary
import codeskulptor
codeskulptor.set_timeout(20)

def gen_all_sequences(outcomes, length):
    """
    Iterative function that enumerates the set of all sequences of
    outcomes of given length.
    """
    answer_set = set([()])
    for dummy_idx in range(length):
        temp_set = set()
        for partial_sequence in answer_set:
            for item in outcomes:
                new_sequence = list(partial_sequence)
                new_sequence.append(item)
                temp_set.add(tuple(new_sequence))
        answer_set = temp_set
    return answer_set

def score(hand):
    """
    Compute the maximal score for a Yahtzee hand according to the
    upper section of the Yahtzee score card.

    hand: full yahtzee hand

    Returns an integer score 
    """
    temp = [0 for _ in range(max(hand))]    
    for value in hand:
        temp[value - 1] += value
    return max(temp)

def expected_value(held_dice, num_die_sides, num_free_dice):
    """
    Compute the expected value of the held_dice given that there
    are num_free_dice to be rolled, each with num_die_sides.

    held_dice: dice that you will hold
    num_die_sides: number of sides on each die
    num_free_dice: number of dice to be rolled

    Returns a floating point expected value
    """
    outcomes = tuple([_ for _ in range(1, num_die_sides + 1)])
    subsets = gen_all_sequences(outcomes, num_free_dice)
    score_sum = 0.0
    for subset in subsets:
        score_sum += score(held_dice + subset)
    return score_sum / len(subsets)


def gen_all_holds(hand):
    """
    Generate all possible choices of dice from hand to hold.

    hand: full yahtzee hand

    Returns a set of tuples, where each tuple is dice to hold
    """
    answer_set = set([()])
    previous_set = set([()])
    for dummy_idx in range(len(hand)):
        temp_set = set()        
        for partial_sequence in previous_set:
            # update hand to remove cards in partial_sequence
            updated_hand = list(hand)
            for elem in partial_sequence:
                updated_hand.remove(elem)
            # generate subsets
            for item in updated_hand:
                new_sequence = list(partial_sequence)
                new_sequence.append(item)
                new_sequence.sort()
                if tuple(new_sequence) not in temp_set:
                    temp_set.add(tuple(new_sequence))
        previous_set = temp_set
        answer_set = answer_set.union(temp_set)
    return answer_set

def strategy(hand, num_die_sides):
    """
    Compute the hold that maximizes the expected value when the
    discarded dice are rolled.

    hand: full yahtzee hand
    num_die_sides: number of sides on each die

    Returns a tuple where the first element is the expected score and
    the second element is a tuple of the dice to hold
    """
    hand_len = len(hand)
    holds = gen_all_holds(hand)
    max_expected_value = float('-inf')
    hold_choice = ()
    for hold in holds:
        value = expected_value(hold, num_die_sides, hand_len - len(hold))
        if value > max_expected_value:
            max_expected_value = value
            hold_choice = hold
    return (max_expected_value, hold_choice)

def run_example():
    """
    Compute the dice to hold and expected score for an example hand
    """
    num_die_sides = 6
    hand = (6, 3, 3, 5, 6)
    hand_score, hold = strategy(hand, num_die_sides)
    print "Best strategy for hand", hand, "is to hold", hold, "with expected score", hand_score
    
    
#run_example()


#import poc_holds_testsuite
#poc_holds_testsuite.run_suite(gen_all_holds)
                                       
    
    
    



