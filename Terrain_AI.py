'''
Large play screen 800x600: (252,251) - (2249,1748) game_coords = [252, 251, 2249, 1748] # Where the game window is on the screen.

play size 300x300 

Once we have the food and head coordinates, a cue will be created of moves that bring the difference berween the coordinates closer.
The moveset will be up,down,left,right. 

Try a HILBERT curve pathfinding algorithm 
ooze(no_water), right angles, wall-hugger, straight line bounce, sidewinder

'''
import numpy as np
from math import isqrt#sqrt
#import matplotlib.pyplot as plt
#from warnings import warn
#import heapq

#import multiprocessing

class Terrain_AI:
    def __init__(self, f_mode=3):
        self.path = []
        self.f_mode = f_mode
        #self.f_mode = 2

    def astar_path(self, maze, start, end, allow_diagonal_movement = False):

        #plt.imshow(maze, cmap='Greys')
        #plt.show()
        
        start = tuple(start)#inputs must be tuples...
        end = tuple(end) 
        maze_g = [50,1,1,1,2,6,100]#Water, beach, sand, grass, forrest, mountains, snow.
        #beach is not used.
        realy_bool = False #if we time out, we hand off the relay.


        def return_path(current_node):
            path = []
            current = current_node
            while current is not None:
                path.append(current["position"])
                current = current["parent"]
            return path[::-1]  # Return reversed path

        def closed_coords(closed_list):
            closed_coords_list = []
            for entry in closed_list:
                closed_coords_list.append(entry["position"])
            return closed_coords_list

        # Create start and end node
        node_template = {   "parent":None,
                            "position":None,
                            "g":0,
                            "h":0,
                            "f":0
                        }

        start_node = node_template.copy()
        start_node["position"] = start

        end_node = node_template.copy()
        end_node["position"] = end

        res_y, res_x = maze.shape[0], maze.shape[1]

        # Initialize both open and closed list
        open_list = []
        closed_list = []

        max_len = 0
        max_len_node = []

        open_list.append(start_node)

        # Adding a stop condition
        outer_iterations = 0
        max_iterations = 1500
        if self.f_mode == 1:
            max_iterations = int(max_iterations*0.4)

        # what squares do we search
        adjacent_squares = ((-1, 0), (1, 0), (0, 1), (0, -1))
        if allow_diagonal_movement:
            adjacent_squares = ((0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1),)

        # Loop until you find the end
        while len(open_list) > 0:
            outer_iterations += 1
            final_bool = False
            if outer_iterations % 100 == 0:
                print(f"Search Cycle: {outer_iterations}")

            
            #failed to find a path
            if outer_iterations > max_iterations:
                #warn("giving up on pathfinding too many iterations")
                print("giving up on pathfinding too many iterations; Max Len Path chosen")
                realy_bool = True
                yield return_path(max_len_node), final_bool, realy_bool
            
                
            
            # Get the current node (lowest f in the open list entries.)
            open_list.sort(key=lambda d: d['f'])
            current_node = open_list.pop(0)
            closed_list.append(current_node)

            # We're tracking longest failed path for contingency
            if len(closed_list) > max_len:
                max_len = len(closed_list)
                max_len_node = current_node.copy()

            # Found the goal
            if current_node["position"] == end_node["position"]:
                final_bool = True
                yield return_path(current_node), final_bool, realy_bool

            # Generate children
            children = [] #This will populate with 4 adjacent nodes if valid.
            
            for new_position in adjacent_squares: # Adjacent squares

                # Get node position
                node_y, node_x = current_node["position"][0] + new_position[0], current_node["position"][1] + new_position[1]
                
                #"""
                # Make sure within range
                if node_y > (res_y-1) or node_y < 0 or node_x > (res_x-1) or node_x < 0:
                    continue

                # Make sure walkable terrain
                terrain_type = maze[node_y][node_x]
                if terrain_type == 6: #6 is snow atop moutains.
                    continue

                # Create new node
                child = { "parent":current_node,
                            "position":(node_y, node_x),
                            "g":0,
                            "h":0,
                            "f":0
                        }

                # Skip if child is on the closed list
                child_pos = child["position"]
                if len([closed_child for closed_child in closed_list if closed_child["position"] == child["position"]]) > 0:
                    continue

                # Create the f, g, and h values
                child["g"] = current_node["g"] + maze_g[terrain_type]
                
                if self.f_mode == 1: #cube
                    child["h"] = ((child_pos[0] - end[0]) ** 2) + ((child_pos[1] - end[1]) ** 2)
                elif self.f_mode == 2: #cube then sqrt
                    child["h"] = maze_g[terrain_type]*isqrt((child_pos[0] - end[0]) ** 2) + ((child_pos[1] - end[1]) ** 2)
                elif self.f_mode == 3: #Manhattan heuristic
                    child["h"] = maze_g[terrain_type]*1.1*(abs(child_pos[0] - end[0]) + abs(child_pos[1] - end[1]))
                
                child["f"] = child["g"] + child["h"]

                # Child is already in the open list
                if len([open_node for open_node in open_list if child["position"] == open_node["position"] and child["g"] > open_node["g"]]) > 0:
                    continue

                # Add the child to the open list
                open_list.append(child)

            yield closed_coords(closed_list), final_bool, realy_bool

        #warn("Couldn't get a path to destination")
        print("Couldn't get a path to destination")
        final_bool = True
        yield closed_coords(closed_list), final_bool, realy_bool

    def smart_blob(self, maze, start, end):

        #plt.imshow(maze, cmap='Greys')
        #plt.show()
        
        start = tuple(start)#inputs must be tuples...
        end = tuple(end) 

        def return_path(current_node):
            path = []
            current = current_node
            while current is not None:
                path.append(current["position"])
                current = current["parent"]
            return path[::-1]  # Return reversed path

        def closed_coords(closed_list):
            closed_coords_list = []
            for entry in closed_list:
                closed_coords_list.append(entry["position"])
            return closed_coords_list

        # Create start and end node
        node_template = {   "parent":None,
                            "position":None,
                            "g":0,
                            "h":0,
                            "f":0
                        }

        start_node = node_template.copy()
        start_node["position"] = start

        end_node = node_template.copy()
        end_node["position"] = end

        res_y, res_x = maze.shape[0], maze.shape[1]

        # Initialize both open and closed list
        open_list = []
        closed_list = []

        max_len = 0
        max_len_node = []

        open_list.append(start_node)

        # Adding a stop condition
        outer_iterations = 0
        max_iterations = 1500
        if self.f_mode == 1:
            max_iterations = int(max_iterations*0.4)

        # what squares do we search
        adjacent_squares = ((-1, 0), (1, 0), (0, 1), (0, -1))
        if allow_diagonal_movement:
            adjacent_squares = ((0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1),)

        # Loop until you find the end
        while len(open_list) > 0:
            outer_iterations += 1
            final_bool = False
            if outer_iterations % 100 == 0:
                print(f"Search Cycle: {outer_iterations}")

            
            #failed to find a path
            if outer_iterations > max_iterations:
                #warn("giving up on pathfinding too many iterations")
                print("giving up on pathfinding too many iterations; Max Len Path chosen")
                realy_bool = True
                yield return_path(max_len_node), final_bool, realy_bool
            
                
            
            # Get the current node (lowest f in the open list entries.)
            open_list.sort(key=lambda d: d['f'])
            current_node = open_list.pop(0)
            closed_list.append(current_node)

            # We're tracking longest failed path for contingency
            if len(closed_list) > max_len:
                max_len = len(closed_list)
                max_len_node = current_node.copy()

            # Found the goal
            if current_node["position"] == end_node["position"]:
                final_bool = True
                yield return_path(current_node), final_bool, realy_bool

            # Generate children
            children = [] #This will populate with 4 adjacent nodes if valid.
            
            for new_position in adjacent_squares: # Adjacent squares

                # Get node position
                node_y, node_x = current_node["position"][0] + new_position[0], current_node["position"][1] + new_position[1]
                
                #"""
                # Make sure within range
                if node_y > (res_y-1) or node_y < 0 or node_x > (res_x-1) or node_x < 0:
                    continue

                # Make sure walkable terrain
                terrain_type = maze[node_y][node_x]
                if terrain_type == 6 or terrain_type == 0: #6 is snow atop moutains.
                    continue

                # Create new node
                child = { "parent":current_node,
                            "position":(node_y, node_x),
                            "g":0,
                            "h":0,
                            "f":0
                        }

                # Skip if child is on the closed list
                child_pos = child["position"]
                if len([closed_child for closed_child in closed_list if closed_child["position"] == child["position"]]) > 0:
                    continue

                # Create the f, g, and h values
                child["g"] = current_node["g"] + maze_g[terrain_type]
                
                if self.f_mode == 1: #cube
                    child["h"] = ((child_pos[0] - end[0]) ** 2) + ((child_pos[1] - end[1]) ** 2)
                elif self.f_mode == 2: #cube then sqrt
                    child["h"] = isqrt((child_pos[0] - end[0]) ** 2) + ((child_pos[1] - end[1]) ** 2)
                elif self.f_mode == 3: #Manhattan heuristic
                    child["h"] = maze_g[terrain_type]*1.1*(abs(child_pos[0] - end[0]) + abs(child_pos[1] - end[1]))
                
                child["f"] = child["g"] + child["h"]

                # Child is already in the open list
                if len([open_node for open_node in open_list if child["position"] == open_node["position"] and child["g"] > open_node["g"]]) > 0:
                    continue

                # Add the child to the open list
                open_list.append(child)

            yield closed_coords(closed_list), final_bool, realy_bool

        #warn("Couldn't get a path to destination")
        print("Couldn't get a path to destination")
        final_bool = True
        yield closed_coords(closed_list), final_bool, realy_bool




def main():
    print("Main not configured")

if __name__ == "__main__":
    main()