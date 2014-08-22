"""
Student facing code for Tantrix Solitaire
http://www.jaapsch.net/puzzles/tantrix.htm

Game is played on a grid of hexagonal tiles.
All ten tiles for Tantrix Solitaire and place in a corner of the grid.
Click on a tile to rotate it.  Cick and drag to move a tile.

Goal is to position the 10 provided tiles to form
a yellow, red or  blue loop of length 10
"""



# Core modeling idea - a triangular grid of hexagonal tiles are 
# model by integer tuples of the form (i, j, k) 
# where i + j + k == size and i, j, k >= 0.

# Each hexagon has a neighbor in one of six directions
# These directions are modeled by the differences between the 
# tuples of these adjacent tiles

# Numbered directions for hexagonal grid, ordered clockwise at 60 degree intervals
DIRECTIONS = {0 : (-1, 0, 1), 1 : (-1, 1, 0), 2 : (0, 1, -1), 
              3 : (1, 0, -1), 4 : (1, -1, 0), 5 : (0,  -1, 1)}

def reverse_direction(direction):
    """
    Helper function that returns opposite direction on hexagonal grid
    """
    num_directions = len(DIRECTIONS)
    return (direction + num_directions / 2) % num_directions

def addTuple(a, b):
    """
    Addition for two tuples
    """
    return tuple(dummya + dummyb for dummya, dummyb in zip(a, b))

# Color codes for ten tiles in Tantrix Solitaire
# "B" denotes "Blue", "R" denotes "Red", "Y" denotes "Yellow"
SOLITAIRE_CODES = ["BBRRYY", "BBRYYR", "BBYRRY", "BRYBYR", "RBYRYB",
                "YBRYRB", "BBRYRY", "BBYRYR", "YYBRBR", "YYRBRB"]


# Minimal size of grid to allow placement of 10 tiles
MINIMAL_GRID_SIZE = 4



class Tantrix:
    """
    Basic Tantrix game class
    """
    
    def __init__(self, size):
        """
        Create a triangular grid of hexagons with size + 1 tiles on each side.
        """
        assert size >= MINIMAL_GRID_SIZE
        self.size = size        
        self.init_tile_index()

        # Initialize dictionary tile_value to contain codes for ten
        # tiles in Solitaire Tantrix in one 4x4 corner of grid
        self.tile_value = {}
        for idx in range(len(SOLITAIRE_CODES)):
            self.tile_value[self.tile_index[idx]] = SOLITAIRE_CODES[idx]

    
    def init_tile_index(self):
        """
        Initialize tile index
        """
        self.tile_index = []
        for col in range(self.size + 1):
            if 0 == col:                
                last_col = [(0, 0, self.size)]
            else:
                curr_col = []
                curr_col.append(addTuple(last_col[0], DIRECTIONS[3]))
                for _tuple in last_col:
                    curr_col.append(addTuple(_tuple, DIRECTIONS[2]))
                last_col = curr_col
            self.tile_index.extend(last_col)

    def __str__(self):
        """
        Return string of dictionary of tile positions and values
        """
        return str(self.tile_value)
        
    def get_tiling_size(self):
        """
        Return size of board for GUI
        """
        return self.size
    
    def tile_exists(self, index):
        """
        Return whether a tile with given index exists
        """
        return index in self.tile_index
    
    def place_tile(self, index, code):
        """
        Play a tile with code at cell with given index
        """
        if self.tile_exists(index):
            self.tile_value[index] = code

    def remove_tile(self, index):
        """
        Remove a tile at cell with given index
        and return the code value for that tile
        """
        if self.tile_exists(index):
            return self.tile_value.pop(index)
               
    def rotate_tile(self, index):
        """
        Rotate a tile clockwise at cell with given index
        """
        if self.tile_exists(index):
            value = self.tile_value[index]
            # rotate the string clockwise
            self.tile_value[index] = value[-1] + value[:-1]

    def get_code(self, index):
        """
        Return the code of the tile at cell with given index
        """
        if self.tile_exists(index):
            if self.tile_value.has_key(index):
                return self.tile_value[index]
            else:
                return ''

    def get_neighbor(self, index, direction):
        """
        Return the index of the tile neighboring the tile with given index in given direction
        """
        if self.tile_exists(index):
            neighbor_index = addTuple(index, DIRECTIONS[direction])
            if self.tile_exists(neighbor_index):
                return neighbor_index
        return ()

    def is_legal(self):
        """
        Check whether a tile configuration obeys color matching rules for adjacent tiles
        """
        for index in self.tile_index:
            self_value = self.get_code(index)
            if self_value:
                for direction in DIRECTIONS:
                    neighbor_index = self.get_neighbor(index, direction)
                    neighbor_value = self.get_code(neighbor_index)
                    if neighbor_value and self_value[direction] != neighbor_value[reverse_direction(direction)]:
                        return False
        return True
            
    def has_loop(self, color):
        """
        Check whether a tile configuration has a loop of size 10 of given color
        """
        # Start from rightmost (0, 0, self.size)
        if not self.is_legal():
            return False
        curr_index = self.tile_index[0]
        curr_value = self.get_code(curr_index)        
        curr_dir = curr_value.index(color)
        loop_list = []
        while curr_value and curr_index != self.tile_index[0]:
            loop_list.append(curr_index)
            curr_index = self.get_neighbor(curr_index, curr_dir)
            curr_value = self.get_node(curr_index)
            if curr_value.index(color) == curr_dir:
                curr_dir = curr_value.rindex(color)
            else:
                curr_dir = curr_value.index(color)
        loop_list.sort()
        origin_list = self.tile_index
        origin_list.sort()
        if loop_list != origin_list:
            return False
        return True

    
# run GUI for Tantrix
import poc_tantrix_gui
poc_tantrix_gui.TantrixGUI(Tantrix(6))
