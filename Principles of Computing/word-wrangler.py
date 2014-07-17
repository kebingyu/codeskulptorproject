"""
Student code for Word Wrangler game
"""

import urllib2
import codeskulptor
import poc_wrangler_provided as provided

WORDFILE = "assets_scrabble_words3.txt"


# Functions to manipulate ordered word lists

def remove_duplicates(list1):
    """
    Eliminate duplicates in a sorted list.

    Returns a new sorted list with the same elements in list1, but
    with no duplicates.

    This function can be iterative.
    """
    new_list = []
    curr_elem = None
    for elem in list1:
        if elem == None or elem != curr_elem:
            curr_elem = elem
            new_list.append(elem)
    return new_list

def intersect(list1, list2):
    """
    Compute the intersection of two sorted lists.

    Returns a new sorted list containing only elements that are in
    both list1 and list2.

    This function can be iterative.
    
    run time: O(m+n)
    """
    new_list = []
    if len(list1) and len(list2):        
        idx1 = 0
        idx2 = 0
        while idx1 < len(list1) and idx2 < len(list2):
            if list1[idx1] == list2[idx2]:
                new_list.append(list1[idx1])
                idx1 += 1
                idx2 += 1
            elif list1[idx1] > list2[idx2]:
                idx2 += 1
            else:
                idx1 += 1
    return new_list

# Functions to perform merge sort

def merge(list1, list2):
    """
    Merge two sorted lists.

    Returns a new sorted list containing all of the elements that
    are in either list1 and list2.

    This function can be iterative.
    
    run time: O(m+n)
    """     
    new_list = []
    idx1 = 0
    idx2 = 0
    while idx1 < len(list1)  and idx2 < len(list2):
        if list1[idx1] < list2[idx2]:
            new_list.append(list1[idx1])
            idx1 += 1
        else:
            new_list.append(list2[idx2])
            idx2 += 1
    new_list.extend(list1[idx1:])
    new_list.extend(list2[idx2:])            
    return new_list
                
def merge_sort(list1):
    """
    Sort the elements of list1.

    Return a new sorted list with the same elements as list1.

    This function should be recursive.
    """
    if len(list1) < 2:
        return list1
    else:
        mid = len(list1) / 2
        return merge(merge_sort(list1[:mid]), merge_sort(list1[mid:]))

# Function to generate all strings for the word wrangler game

def gen_all_strings(word):
    """
    Generate all strings that can be composed from the letters in word
    in any order.

    Returns a list of all strings that can be formed from the letters
    in word.

    This function should be recursive.
    """ 
    if len(word) == 0:
        return [word]
    elif len(word) == 1:
        return ['', word]
    else:
        first = word[0]
        rest = word[1:]        
        rest_list = gen_all_strings(rest)
        for elem in rest_list[:]:
            elem_len = len(elem)
            for idx in range(elem_len + 1):
                new_string = elem[:idx] + first + elem[idx:]
                rest_list.append(new_string)
        return rest_list

# Function to load words from a file

def load_words(filename):
    """
    Load word list from the file named filename.

    Returns a list of strings.
    """
    url = codeskulptor.file2url(filename)
    netfile = urllib2.urlopen(url);
    words = []
    for line in netfile.readlines():        
        words.append(line[:-1])
    return words

def run():
    """
    Run game.
    """
    words = load_words(WORDFILE)
    wrangler = provided.WordWrangler(words, remove_duplicates, 
                                     intersect, merge_sort, 
                                     gen_all_strings)
    provided.run_game(wrangler)

# Uncomment when you are ready to try the game
run()
