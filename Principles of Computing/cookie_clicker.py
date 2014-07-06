"""
Cookie Clicker Simulator
"""

import simpleplot
import math

# Used to increase the timeout, if necessary
import codeskulptor
codeskulptor.set_timeout(20)

import poc_clicker_provided as provided

# Constants
SIM_TIME = 10000000000.0

class ClickerState:
    """
    Simple class to keep track of the game state.
    During a simulation, upgrades are only allowed at an integral number 
    of seconds as required in Cookie Clicker.
    """
    
    def __init__(self):
        self._total_cookies_produced = 0.0
        self._current_cookies = 0.0
        self._current_time = 0.0
        self._current_cps = 1.0 # cookie per second
        self._history = [(0.0, None, 0.0, 0.0)]
        
    def __str__(self):
        """
        Return human readable state
        """
        print "Time:", self._current_time
        print "Current Cookies:", self._current_cookies
        print "CPS:", self._current_cps
        print "Total Cookies:", self._total_cookies_produced     
        return ""
        
    def get_cookies(self):
        """
        Return current number of cookies 
        (not total number of cookies)
        
        Should return a float
        """
        return self._current_cookies
    
    def get_cps(self):
        """
        Get current CPS

        Should return a float
        """
        return self._current_cps
    
    def get_time(self):
        """
        Get current time

        Should return a float
        """
        return self._current_time
    
    def get_history(self):
        """
        Return history list

        History list should be a list of tuples of the form:
        (time, item, cost of item, total cookies)

        For example: (0.0, None, 0.0, 0.0)
        """
        return self._history

    def time_until(self, cookies):
        """
        Return time until you have the given number of cookies
        (could be 0 if you already have enough cookies)

        Should return a float with no fractional part
        """
        if cookies - self._current_cookies < 0:
            return 0.0
        else:
            return math.ceil((cookies - self._current_cookies) / self._current_cps)
    
    def wait(self, time):
        """
        Wait for given amount of time and update state

        Should do nothing if time <= 0
        """
        if time > 0:
            self._current_time += time
            cookies_produced = time * self._current_cps
            self._current_cookies += cookies_produced
            self._total_cookies_produced += cookies_produced
    
    def buy_item(self, item_name, cost, additional_cps):
        """
        Buy an item and update state

        Should do nothing if you cannot afford the item
        """
        if self._current_cookies >= cost:
            self._current_cookies -= cost
            self._current_cps += additional_cps
            self._history.append((self._current_time, item_name,
                                 cost, self._total_cookies_produced))
   
    
def simulate_clicker(build_info, duration, strategy):
    """
    Function to run a Cookie Clicker game for the given
    duration with the given strategy.  Returns a ClickerState
    object corresponding to game.
    """

    build_info_clone = build_info.clone()
    clicker = ClickerState()
    while clicker.get_time() <= duration:
        # get update info
        item = strategy(clicker.get_cookies(), clicker.get_cps(), 
                 duration - clicker.get_time(), build_info_clone)
        # break if no more items will be purchased
        if None == item:
            break
        item_cost = build_info_clone.get_cost(item)
        # wait until enough cookies
        wait_time = clicker.time_until(item_cost)
        # break if wait past the duration
        if wait_time + clicker.get_time() > duration:
            break
        clicker.wait(wait_time)
        # ready to update
        clicker.buy_item(item, item_cost, build_info_clone.get_cps(item))
        # update build info
        build_info_clone.update_item(item)
    # if there is still time left
    after_loop_cookies = clicker.get_cookies()
    item = strategy(after_loop_cookies, clicker.get_cps(), 
                 duration - clicker.get_time(), build_info_clone)
    if item != None:
        item_cost = build_info_clone.get_cost(item)
        if after_loop_cookies >= item_cost:
            buy_count = int(math.floor(after_loop_cookies / item_cost))
            for dummy_idx in range(buy_count):
                clicker.buy_item(item, item_cost, build_info_clone.get_cps(item))
    clicker.wait(duration - clicker.get_time())
    return clicker


def strategy_cursor(cookies, cps, time_left, build_info):
    """
    Always pick Cursor!

    Note that this simplistic strategy does not properly check whether
    it can actually buy a Cursor in the time left.  Your strategy
    functions must do this and return None rather than an item you
    can't buy in the time left.
    """
    return "Cursor"

def strategy_none(cookies, cps, time_left, build_info):
    """
    Always return None

    This is a pointless strategy that you can use to help debug
    your simulate_clicker function.
    """
    return None

def strategy_cheap(cookies, cps, time_left, build_info):
    """
    this strategy should always select the cheapest item that you can afford in the time left
    """
    return_item = None
    lowest_cost = float('inf')
    item_list = build_info.build_items()
    cookies_potential = cookies + time_left * cps
    for item in item_list:
        cost = build_info.get_cost(item)
        if cookies_potential >= cost and cost < lowest_cost:
            return_item = item
            lowest_cost = cost
    return return_item

def strategy_expensive(cookies, cps, time_left, build_info):
    """
    this strategy should always select the most expensive item you can afford in the time left
    """
    return_item = None
    highest_cost = float('-inf')
    item_list = build_info.build_items()
    cookies_potential = cookies + time_left * cps
    for item in item_list:
        cost = build_info.get_cost(item)
        if cookies_potential >= cost and cost > highest_cost:
            return_item = item
            highest_cost = cost
    return return_item

def strategy_best(cookies, cps, time_left, build_info):
    """
    this is the best strategy that you can come up with
    """
    return_item = None
    highest_icr = float('-inf')
    item_list = build_info.build_items()
    cookies_potential = cookies + time_left * cps
    for item in item_list:
        cost = build_info.get_cost(item)
        curr_icr = build_info.get_cps(item) / cost        
        if cookies_potential >= cost and curr_icr > highest_icr:
            return_item = item
            highest_icr = curr_icr
    return return_item
        
def run_strategy(strategy_name, time, strategy):
    """
    Run a simulation with one strategy
    """
    state = simulate_clicker(provided.BuildInfo(), time, strategy)
    print strategy_name, ":", state

    # Plot total cookies over time

    # Uncomment out the lines below to see a plot of total cookies vs. time
    # Be sure to allow popups, if you do want to see it

    history = state.get_history()
    history = [(item[0], item[3]) for item in history]
    simpleplot.plot_lines(strategy_name, 1000, 400, 'Time', 'Total Cookies', [history], True)

def run():
    """
    Run the simulator.
    """    
    #run_strategy("Cursor", SIM_TIME, strategy_cursor)

    # Add calls to run_strategy to run additional strategies
    run_strategy("Cheap", SIM_TIME, strategy_cheap)
    run_strategy("Expensive", SIM_TIME, strategy_expensive)
    run_strategy("Best", SIM_TIME, strategy_best)
    
run()
    

