"""
Loyd's Fifteen puzzle - solver and visualizer
Note that solved configuration has the blank (zero) tile in upper left
Use the arrows key to swap this tile with its neighbors
"""

import poc_fifteen_gui

#cyclic moves dictionary
CYCLIC = {
          # zero on the left of target, zero move upwards to move target to the right
          'same_row_left_u' : 'urrdl',
          # zero on the left of target, zero move downwards to move target to the right
          'same_row_left_d' : 'drrul',
          # zero on the left of target, zero move downwards to move target to the left
          'same_row_left_d_l' : 'rdllu',
          # zero on the right of target, zero move upwards to move target to the left
          'same_row_right_u' : 'ulldr',
          # zero on the right of target, zero move downwards to move target to the left
          'same_row_right_d' : 'dllur',
          # zero on the left of target, zero move downwards to move target down
          'same_row_left_move_down' : 'druld',
          # zero on the right of target, zero move downwards to move target down
          'same_row_right_move_down' : 'dlurd',
          # cyclic 2*2
          'two_by_two' : 'rdlu'
          }

class Puzzle:
    """
    Class representation for the Fifteen puzzle
    """

    def __init__(self, puzzle_height, puzzle_width, initial_grid=None):
        """
        Initialize puzzle with default height and width
        Returns a Puzzle object
        """
        self._height = puzzle_height
        self._width = puzzle_width
        self._grid = [[col + puzzle_width * row
                       for col in range(self._width)]
                      for row in range(self._height)]

        if initial_grid != None:
            for row in range(puzzle_height):
                for col in range(puzzle_width):
                    self._grid[row][col] = initial_grid[row][col]

    def __str__(self):
        """
        Generate string representaion for puzzle
        Returns a string
        """
        ans = ""
        for row in range(self._height):
            ans += str(self._grid[row])
            ans += "\n"
        return ans

    #####################################
    # GUI methods

    def get_height(self):
        """
        Getter for puzzle height
        Returns an integer
        """
        return self._height

    def get_width(self):
        """
        Getter for puzzle width
        Returns an integer
        """
        return self._width

    def get_number(self, row, col):
        """
        Getter for the number at tile position pos
        Returns an integer
        """
        return self._grid[row][col]

    def set_number(self, row, col, value):
        """
        Setter for the number at tile position pos
        """
        self._grid[row][col] = value

    def clone(self):
        """
        Make a copy of the puzzle to update during solving
        Returns a Puzzle object
        """
        new_puzzle = Puzzle(self._height, self._width, self._grid)
        return new_puzzle

    ########################################################
    # Core puzzle methods

    def current_position(self, solved_row, solved_col):
        """
        Locate the current position of the tile that will be at
        position (solved_row, solved_col) when the puzzle is solved
        Returns a tuple of two integers        
        """
        solved_value = (solved_col + self._width * solved_row)

        for row in range(self._height):
            for col in range(self._width):
                if self._grid[row][col] == solved_value:
                    return (row, col)
        assert False, "Value " + str(solved_value) + " not found"

    def update_puzzle(self, move_string):
        """
        Updates the puzzle state based on the provided move string
        """
        zero_row, zero_col = self.current_position(0, 0)
        for direction in move_string:
            if direction == "l":
                assert zero_col > 0, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row][zero_col - 1]
                self._grid[zero_row][zero_col - 1] = 0
                zero_col -= 1
            elif direction == "r":
                assert zero_col < self._width - 1, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row][zero_col + 1]
                self._grid[zero_row][zero_col + 1] = 0
                zero_col += 1
            elif direction == "u":
                assert zero_row > 0, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row - 1][zero_col]
                self._grid[zero_row - 1][zero_col] = 0
                zero_row -= 1
            elif direction == "d":
                assert zero_row < self._height - 1, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row + 1][zero_col]
                self._grid[zero_row + 1][zero_col] = 0
                zero_row += 1
            else:
                assert False, "invalid direction: " + direction

    ##################################################################
    # Phase one methods

    def lower_row_invariant(self, target_row, target_col):
        """
        Check whether the puzzle satisfies the specified invariant
        at the given position in the bottom rows of the puzzle (target_row > 1)
        Returns a boolean
        """
        # check if Tile zero is positioned at (i,j)
        if self.get_number(target_row, target_col) != 0:
            return False
        # check if All tiles in rows i+1 or below are positioned at their 
        # solved location.
        height = self.get_height()
        width  = self.get_width()
        for row in range(target_row + 1, height):
            for col in range(width):
                if self.get_number(row, col) != col + width * row:
                    return False
        # check if All tiles in row i to the right of position (i,j) are 
        # positioned at their solved location.
        for col in range(target_col + 1, width):
            if self.get_number(target_row, col) != col + width * target_row:
                return False
        return True

    def solve_interior_tile(self, target_row, target_col):
        """
        Place correct tile at target position
        Updates puzzle and returns a move string
        """
        assert self.lower_row_invariant(target_row, target_col)
        assert target_col > 0
        moves = ''
        # get current position of target tile
        curr_row, curr_col = self.current_position(target_row, target_col)
        
        # target tile is at the same row to the left
        if curr_row == target_row:
            assert curr_col < target_col
            # first move zero to the left of the target tile
            moves += (target_col - curr_col) * 'l'
            # next series of cyclic moves to the zero tile that move the target 
            # tile back to the target position one position at a time
            moves += (target_col - (curr_col + 1)) * CYCLIC['same_row_left_u']
            # and we are done       
            
        # target tile is above zero tile
        else:
            assert curr_row < target_row
            # first we always move zero to the left of target tile, both on curr_row
            # target on the right
            if curr_col > target_col:
                moves += (target_row - curr_row) * 'u'
                moves += (curr_col - target_col) * 'r'
                if curr_row == target_row - 1:
                    # zero has to move upwards so that the already done tiles are not broken
                    moves += ((curr_col - 1) - target_col) * CYCLIC['same_row_right_u']
                    # move zero to the left of target
                    moves += 'ulld'
                else:
                    moves += ((curr_col - 1) - target_col) * CYCLIC['same_row_right_d']
                    # move zero to the left of target
                    moves += 'dllu'    
            # target on the left
            elif curr_col < target_col:
                moves += (target_row - curr_row) * 'u'
                moves += (target_col - curr_col) * 'l'
                if curr_row == target_row - 1:
                    # zero has to move upwards so that the already done tiles are not broken
                    moves += (target_col - (curr_col + 1)) * CYCLIC['same_row_left_u']
                else:
                    moves += (target_col - (curr_col + 1)) * CYCLIC['same_row_left_d']
                # zero already on the left of target, no need to move
            # target is right above
            else: 
                # move zero to the left of target
                moves += (target_row - (curr_row + 1)) * 'u'
                moves += 'lu'
            # then cyclic moves target tile down to the target position
            moves += (target_row - curr_row) * CYCLIC['same_row_left_move_down']
            # and we are done            
            
        self.update_puzzle(moves)
        assert self.lower_row_invariant(target_row, target_col - 1)
        return moves

    def solve_col0_tile(self, target_row):
        """
        Solve tile in column zero on specified row (> 1)
        Updates puzzle and returns a move string
        """
        assert self.lower_row_invariant(target_row, 0)
        # move the zero tile from (i,0) to (i+1,1)
        moves = 'ur'
        self.update_puzzle(moves)
        moves = ''
        # get current position of target tile
        curr_row, curr_col = self.current_position(target_row, 0)
        if curr_row == target_row and curr_col == 0: # lucky!
            moves += ''
        else:
            # first reposition target tile to position (i-1,1) and zero tile to position (i-1,0)
            # always move zero to the left of target, then runs cyclic moves
            # target on the left
            if curr_col < 1:
                moves += ((target_row - 1) - curr_row) * 'u'
                moves += 'l'
            # target on the right
            elif curr_col > 1:
                moves += ((target_row - 1) - curr_row) * 'u'
                moves += (curr_col - 2) * 'r'
                moves += (curr_col - 1) * CYCLIC['same_row_left_d_l']
            # target is above
            else:
                moves += ((target_row - 2) - curr_row) * 'u'
                moves += 'lu'
            # cyclic
            moves += ((target_row - 1) - curr_row) * CYCLIC['same_row_left_move_down']
            # apply 3*2 secret move
            moves += 'ruldrdlurdluurddlur'
        # move zero to (i-1,n-1) and we are done
        moves += (self.get_width() - 2) * 'r'
        self.update_puzzle(moves)
        assert self.lower_row_invariant(target_row - 1, self.get_width() - 1)
        return 'ur' + moves

    #############################################################
    # Phase two methods

    def row0_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row zero invariant
        at the given column (col > 1)
        Returns a boolean
        """
        if self.get_number(0, target_col) != 0:
            return False
        # check if All tiles in rows 2 or below are positioned at their 
        # solved location.
        height = self.get_height()
        width  = self.get_width()
        for row in range(2, height):
            for col in range(width):
                if self.get_number(row, col) != col + width * row:
                    return False
        # check if All tiles from (0,j+1) to (0,n-1) and (1,j) to (1,n-1) are 
        # positioned at their solved location.
        for col in range(target_col + 1, width):
            if self.get_number(0, col) != col + width * 0:
                return False
        for col in range(target_col, width):
            if self.get_number(1, col) != col + width * 1:
                return False
        return True

    def row1_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row one invariant
        at the given column (col > 1)
        Returns a boolean
        """
        return self.lower_row_invariant(1, target_col)

    def solve_row0_tile(self, target_col):
        """
        Solve the tile in row zero at the specified column
        Updates puzzle and returns a move string
        """
        assert self.row0_invariant(target_col)
        assert target_col > 1
        # move the zero tile from (0,j) to (1,j-1)
        moves = 'ld'
        self.update_puzzle(moves)
        moves = ''
        # get current position of target tile
        curr_row, curr_col = self.current_position(0, target_col)
        if curr_row == 0 and curr_col == target_col: # lucky!
            moves += ''
        else:
            # reposition the target tile to position (1,j-1) 
            # with tile zero in position (1,j-2)
            if curr_col == target_col - 1: # above
                moves += 'uld'
            elif curr_col < target_col - 1: # left
                moves += (1 - curr_row) * 'u'
                moves += ((target_col - 1) - curr_col) * 'l'
                if curr_row == 0:
                    moves += ((target_col - 2) - curr_col) * CYCLIC['same_row_left_d']
                else:
                    moves += ((target_col - 2) - curr_col) * CYCLIC['same_row_left_u']
            else:
                moves += None
            # then apply 2*3 secrect move
            moves += 'urdlurrdluldrruld'
        # and we are done        
        self.update_puzzle(moves)
        assert self.row1_invariant(target_col - 1)
        return 'ld' + moves

    def solve_row1_tile(self, target_col):
        """
        Solve the tile in row one at the specified column
        Updates puzzle and returns a move string
        """
        assert self.row1_invariant(target_col)
        assert target_col > 1
        target_row = 1
        moves = ''
        # get current position of target tile
        curr_row, curr_col = self.current_position(target_row, target_col)
        
        # target tile is at the same row to the left (row 1)
        if curr_row == target_row:
            assert curr_col < target_col
            # first move zero to the left of the target tile
            moves += (target_col - curr_col) * 'l'
            # next series of cyclic moves to the zero tile that move the target 
            # tile back to the target position one position at a time
            moves += (target_col - (curr_col + 1)) * CYCLIC['same_row_left_u']
            # move zero tile to (0, target_col) and we are done       
            moves += 'ur'
            
        # target tile is above zero tile (row 0)
        else:
            assert curr_row < target_row
            # depends on where the target tile is
            if curr_col > target_col:
                moves += None    
            # target on the left
            elif curr_col < target_col:
                moves += (target_row - curr_row) * 'u'
                moves += (target_col - curr_col) * 'l'
                moves += (target_col - (curr_col + 1)) * CYCLIC['same_row_left_d']
                moves += 'dru'
            # target is right above
            else:                 
                moves += 'u'                     
            # and we are done            
            
        self.update_puzzle(moves)
        assert self.row0_invariant(target_col)
        return moves

    ###########################################################
    # Phase 3 methods

    def solve_2x2(self):
        """
        Solve the upper left 2x2 part of the puzzle
        Updates the puzzle and returns a move string
        """
        assert self.row1_invariant(1)
        # move zero to (0,0)
        moves = 'lu'
        self.update_puzzle(moves)
        if self.two_by_two_invariant():
            return moves;
        else:
            # apply at most two 2*2 cyclic moves
            step = 2
            moves = ''
            while step > 0:
                moves += CYCLIC['two_by_two']
                self.update_puzzle(moves)
                if self.two_by_two_invariant():
                    return 'lu' + moves
                else:
                    step -= 1
            # unsolveable
            return ''

    def solve_puzzle(self):
        """
        Generate a solution string for a puzzle
        Updates the puzzle and returns a move string
        """
        moves = ''
        width = self.get_width()
        height = self.get_height()
        # phase one
        for row in range(height - 1, 1, -1):
            for col in range(width - 1, 0, -1):
                moves += self.solve_interior_tile(row, col)
                print self
            moves += self.solve_col0_tile(row)
            print self
        # phase two
        for col in range(width - 1, 1, -1):
            moves += self.solve_row1_tile(col)
            print self
            moves += self.solve_row0_tile(col)
            print self
        # phase one
        moves += self.solve_2x2()
        return moves
    
    def two_by_two_invariant(self):
        """
        Check if 2x2 is solved
        """
        width = self.get_width()
        if self.get_number(0, 0) == 0 and \
            self.get_number(0, 1) == 1 and \
            self.get_number(1, 0) == width and \
            self.get_number(1, 1) == 1 + width:
                return True
        return False

# Start interactive simulation
#poc_fifteen_gui.FifteenGUI(Puzzle(2, 3))
p = Puzzle(3, 3, [[8, 7, 6], [5, 4, 3], [2, 1, 0]])
p.solve_puzzle()
print p

p = Puzzle(4,4, [[8,2,9,15],[4,6,7,12],[5,3,10,11],[1,13,14,0]])
print p
p.solve_interior_tile(3, 3)
print p
p.solve_interior_tile(3, 2)
print p
p.solve_interior_tile(3, 1)
print p
p.solve_col0_tile(3)
print p
p.solve_interior_tile(2, 3)
print p
p.solve_interior_tile(2, 2)
print p
p.solve_interior_tile(2, 1)
print p
p.solve_col0_tile(2)
print p

p.solve_row1_tile(3)
print p
p.solve_row0_tile(3)
print p
p.solve_row1_tile(2)
print p
p.solve_row0_tile(2)
print p

p.solve_2x2()
print p


