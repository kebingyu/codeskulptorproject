"""
Student portion of Zombie Apocalypse mini-project
"""

import random
import poc_grid
import poc_queue
import poc_zombie_gui

# global constants
EMPTY = 0 
FULL = 1
FOUR_WAY = 0
EIGHT_WAY = 1
OBSTACLE = "obstacle"
HUMAN = "human"
ZOMBIE = "zombie"


class Zombie(poc_grid.Grid):
    """
    Class for simulating zombie pursuit of human on grid with
    obstacles
    """

    def __init__(self, grid_height, grid_width, obstacle_list = None, 
                 zombie_list = None, human_list = None):
        """
        Create a simulation of given size with given obstacles,
        humans, and zombies
        """
        poc_grid.Grid.__init__(self, grid_height, grid_width)
        if obstacle_list != None:
            for cell in obstacle_list:
                self.set_full(cell[0], cell[1])
        if zombie_list != None:
            self._zombie_list = list(zombie_list)
        else:
            self._zombie_list = []
        if human_list != None:
            self._human_list = list(human_list)  
        else:
            self._human_list = []
        
    def clear(self):
        """
        Set cells in obstacle grid to be empty
        Reset zombie and human lists to be empty
        """
        self._zombie_list = []
        self._human_list = []
        poc_grid.Grid.clear(self)
        
    def add_zombie(self, row, col):
        """
        Add zombie to the zombie list
        """
        self._zombie_list.append((row, col))
                
    def num_zombies(self):
        """
        Return number of zombies
        """
        return len(self._zombie_list)
          
    def zombies(self):
        """
        Generator that yields the zombies in the order they were
        added.
        """
        return (_ for _ in self._zombie_list)

    def add_human(self, row, col):
        """
        Add human to the human list
        """
        self._human_list.append((row, col))
        
    def num_humans(self):
        """
        Return number of humans
        """
        return len(self._human_list)
    
    def humans(self):
        """
        Generator that yields the humans in the order they were added.
        """
        return (_ for _ in self._human_list)
        
    def compute_distance_field(self, entity_type):
        """
        Function computes a 2D distance field
        Distance at member of entity_queue is zero
        Shortest paths avoid obstacles and use distance_type distances
        """
        distance_field = [[self._grid_height * self._grid_width for _ in range(self._grid_width)]
                          for _ in range(self._grid_height)]
        visited = poc_grid.Grid(self._grid_height, self._grid_width)
        if HUMAN == entity_type:
            boundary_list = self.humans()
        elif ZOMBIE == entity_type:
            boundary_list = self.zombies()
        boundary = poc_queue.Queue()
        for position in boundary_list:
            boundary.enqueue(position)
            distance_field[position[0]][position[1]] = 0
            visited.set_full(position[0], position[1])
        while len(boundary):
            curr_cell = boundary.dequeue()
            for neighbor in self.four_neighbors(curr_cell[0], curr_cell[1]):
                # if not a obstacle and not visited
                if self.is_empty(neighbor[0], neighbor[1]) and visited.is_empty(neighbor[0], neighbor[1]):
                    visited.set_full(neighbor[0], neighbor[1])
                    distance_field[neighbor[0]][neighbor[1]] = min(distance_field[neighbor[0]][neighbor[1]],
                                                   distance_field[curr_cell[0]][curr_cell[1]] + 1)
                    boundary.enqueue(neighbor)
        return distance_field
    
    def move_humans(self, zombie_distance):
        """
        Function that moves humans away from zombies, diagonal moves
        are allowed
        """
        updated_human_list = []
        for human in self.humans():
            # find the largest distance in 8 neighbor cells
            max_distance = 0
            max_dist_cell = [(human[0], human[1])]
            # loop through neighbor cells
            for cell in self.eight_neighbors(human[0], human[1]):
                if self.is_empty(cell[0], cell[1]):
                    distance = zombie_distance[cell[0]][cell[1]]
                    if distance == max_distance:
                        max_dist_cell.append(cell)
                    elif distance > max_distance:
                        max_dist_cell = [cell]
                        max_distance = distance
            # decide which cell to move to
            updated_human_list.append(max_dist_cell[random.randrange(len(max_dist_cell))])
        self._human_list = updated_human_list
    
    def move_zombies(self, human_distance):
        """
        Function that moves zombies towards humans, no diagonal moves
        are allowed
        """
        updated_zombie_list = []
        for zombie in self.zombies():
            # find the smallest distance in 4 neighbor cells
            min_distance = human_distance[zombie[0]][zombie[1]]
            min_dist_cell = [zombie]
            # loop through neighbor cells
            for cell in self.four_neighbors(zombie[0], zombie[1]):
                if self.is_empty(cell[0], cell[1]):
                    distance = human_distance[cell[0]][cell[1]]
                    if distance == min_distance:
                        min_dist_cell.append(cell)
                    elif distance < min_distance:
                        min_dist_cell = [cell]
                        min_distance = distance
            # decide which cell to move to
            updated_zombie_list.append(min_dist_cell[random.randrange(len(min_dist_cell))])
        self._zombie_list = updated_zombie_list

# Start up gui for simulation - You will need to write some code above
# before this will work without errors

poc_zombie_gui.run_gui(Zombie(30, 40))

