"""
Clone of 2048 game.
"""

import poc_2048_gui
import random

# Directions, DO NOT MODIFY
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

# Offsets for computing tile indices in each direction.
# DO NOT MODIFY this dictionary.    
OFFSETS = {UP: (1, 0), 
           DOWN: (-1, 0), 
           LEFT: (0, 1), 
           RIGHT: (0, -1)} 
   
def merge(line):
    """
    Helper function that merges a single row or column in 2048
    [2, 2, 2, 2] should return [4, 4, 0, 0] not [4, 2, 2, 0]
    """
    merged_line = [0] * len(line)
    merged = [False] * len(line)
    last_elem = 0
    last_idx = 0
    curr_idx = 0
    for curr_elem in line:
        if curr_elem:
            if not merged[last_idx] and curr_elem == last_elem:
                merged_line[last_idx] = curr_elem + last_elem
                merged[last_idx] = True
            else:
                merged_line[curr_idx] = curr_elem
                last_elem = curr_elem
                last_idx = curr_idx
                curr_idx += 1
    return merged_line
    

class TwentyFortyEight:
    """
    Class to run the game logic.
    """

    def __init__(self, grid_height, grid_width):
        self.height = grid_height
        self.width = grid_width
        self.reset()
        self.set_initial_tiles()
        self.set_merge_line_length()
    
    def reset(self):
        """
        Reset the game so the grid is empty.
        """
        self.cells = [0] * self.height
        for idx in range(self.height):
            self.cells[idx] = [0] * self.width
            
    def set_initial_tiles(self):
        """
        pre-computing a list of the indices for the initial tiles
        """
        self.initial_tiles = {UP:[],DOWN:[],LEFT:[],RIGHT:[]}
        for idx in range(self.width):
            self.initial_tiles[UP].append((0, idx))
            self.initial_tiles[DOWN].append((self.height - 1, idx))
        for idx in range(self.height):
            self.initial_tiles[LEFT].append((idx, 0))
            self.initial_tiles[RIGHT].append((idx, self.width - 1))
            
    def set_merge_line_length(self):
        """
        pre-set the length of the merge line for different direction
        """
        self.merge_line_length = {UP: self.height, 
           DOWN: self.height, 
           LEFT: self.width, 
           RIGHT: self.width}
    
    def __str__(self):
        """
        Return a string representation of the grid for debugging.
        """
        print self.cells
        #print self.initial_tiles
        #print 'row:', self.height, 'column:', self.width
        return ''

    def get_grid_height(self):
        """
        return grid height
        """
        return self.height
    
    def get_grid_width(self):
        """
        return grid width
        """
        return self.width
                            
    def move(self, direction):
        """
        Move all tiles in the given direction and add
        a new tile if any tiles moved.
        """
        changed = False
        init_tile = self.initial_tiles[direction]
        offset = OFFSETS[direction]
        total_merge = len(init_tile)
        merge_line_length = self.merge_line_length[direction]
        for idx in range(total_merge):
            init_tile_tuple = init_tile[idx]            
            curr_tile_tuple = []
            # get current tile tuple based on offset
            for dummy_i in range(merge_line_length):
                row = init_tile_tuple[0] + offset[0] * dummy_i
                col = init_tile_tuple[1] + offset[1] * dummy_i
                curr_tile_tuple.append((row, col))
            # fill current tile
            curr_tile = []
            for dummy_i in range(merge_line_length):
                row = curr_tile_tuple[dummy_i][0]
                col = curr_tile_tuple[dummy_i][1]
                curr_tile.append(self.get_tile(row, col))  
            # merge
            new_tile = merge(curr_tile)
            # put merged tile back to the grid
            for dummy_i in range(merge_line_length):
                row = curr_tile_tuple[dummy_i][0]
                col = curr_tile_tuple[dummy_i][1]
                self.set_tile(row, col, new_tile[dummy_i])            
            # check if changed
            if new_tile != curr_tile:
                changed = True
        if changed:
            self.new_tile()
        
    def new_tile(self):
        """
        Create a new tile in a randomly selected empty 
        square.  The tile should be 2 90% of the time and
        4 10% of the time.
        """        
        selected = False
        while not selected:
            row = random.randrange(0, self.height)
            col = random.randrange(0, self.width)
            if self.get_tile(row, col) == 0:
                value = random.random()
                if value <= 0.1:
                    self.set_tile(row, col, 4)
                else:
                    self.set_tile(row, col, 2)
                selected = True
        
    def set_tile(self, row, col, value):
        """
        Set the tile at position row, col to have the given value.
        """        
        self.cells[row][col] = value

    def get_tile(self, row, col):
        """
        Return the value of the tile at position row, col.
        """        
        return self.cells[row][col] 
    
poc_2048_gui.run_gui(TwentyFortyEight(4, 5))


