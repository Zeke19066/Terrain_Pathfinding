import noise
import numpy as np
from PIL import Image
import math
import random
import matplotlib.pyplot as plt
import cv2

#https://medium.com/@yvanscher/playing-with-perlin-noise-generating-realistic-archipelagos-b59f004d8401

#we need a distribution of th maze values.

class Terrain_Generator():
    def __init__(self, res_y, res_x):

        self.color_dict = {
                        "beach":(238, 214, 175),
                        "snow":(255, 250, 250),
                        "mountain":(139, 137, 137),
                        "lightblue":(0,191,255),
                        "blue":(65,105,225),
                        "green":(34,139,34),
                        "darkgreen":(0,100,0),
                        "sandy":(210,180,140),
                        "red":(255,0,0)
                        }

        self.shape = (1024,1024)
        self.final_rez_y, self.final_rez_x = res_y, res_x
        #self.slice_off = int((self.shape[0]-self.final_rez_x)/2)
        self.slice_off = 250
        self.scale = 100 #100
        self.show_the_process = False
        self.octaves = 6
        #self.threshold = np.random.randint(5,20) #affects land/island ratio
        self.threshold = 5
        self.persistence = 0.5
        self.lacunarity = 2.0
        self.seed = np.random.randint(0,500) #seed for the noise generator.
        #self.seed = 126 #seed for the noise generator.

    def rgb_norm(self, world):
        world_min = np.min(world)
        world_max = np.max(world)
        norm = lambda x: (x-world_min/(world_max - world_min))*255
        return np.vectorize(norm)

    def prep_world(self, world):
        norm = self.rgb_norm(world)
        world = norm(world)
        return world

    def add_color(self, world):
        shape = world.shape
        color_world = np.zeros(world.shape+(3,))
        for i in range(shape[0]):
            for j in range(shape[1]):
                if world[i][j] < -0.05:
                    color_world[i][j] = self.color_dict["blue"]
                elif world[i][j] < 0:
                    color_world[i][j] = self.color_dict["beach"]
                elif world[i][j] < .20:
                    color_world[i][j] = self.color_dict["green"]
                elif world[i][j] < 0.35:
                    color_world[i][j] = self.color_dict["mountain"]
                elif world[i][j] < 1.0:
                    color_world[i][j] = self.color_dict["snow"]
        return color_world

    def add_color2(self, world, colors):
        shape = world.shape
        color_world = np.zeros(world.shape+(3,))
        if colors[0] == 0:
            color_world = np.zeros(world.shape)
        for i in range(shape[0]):
            for j in range(shape[1]):
                if world[i][j] < self.threshold + 99: #Water 100
                    color_world[i][j] = colors[0] 
                #lif world[i][j] < self.threshold + 102: #Beach 102
                #    color_world[i][j] = colors[1]
                elif world[i][j] < self.threshold + 104: #Sand 104
                    color_world[i][j] = colors[2]
                elif world[i][j] < self.threshold + 115: #Grass
                    color_world[i][j] = colors[3]
                elif world[i][j] < self.threshold + 130: #Forrest
                    color_world[i][j] = colors[4]
                elif world[i][j] < self.threshold + 137: #Mountain
                    color_world[i][j] = colors[5]
                else:
                    color_world[i][j] = colors[6] #Snow

        return color_world

    def generator(self):
        self.seed = np.random.randint(0,500) #seed for the noise generator.
        world = np.zeros(self.shape)
        for i in range(self.shape[0]):
            for j in range(self.shape[1]):
                world[i][j] = noise.pnoise2(i/self.scale, 
                                            j/self.scale, 
                                            octaves=self.octaves, 
                                            persistence=self.persistence, 
                                            lacunarity=self.lacunarity, 
                                            repeatx=1024, 
                                            repeaty=1024, 
                                            base=self.seed)

        if self.show_the_process:
            Image.fromarray(self.prep_world(world)).show()
            color_world = self.add_color(world).astype(np.uint8)
            Image.fromarray(color_world,'RGB').show()

        a,b = self.shape[0]/2, self.shape[1]/2
        n = 1024
        r = 125
        y,x = np.ogrid[-a:n-a, -b:n-b]
        # creates a mask with True False values
        # at indices

        center_x, center_y = self.shape[1] // 2, self.shape[0] // 2
        circle_grad = np.zeros_like(world)

        for y in range(world.shape[0]):
            for x in range(world.shape[1]):
                distx = abs(x - center_x)
                disty = abs(y - center_y)
                dist = math.sqrt(distx*distx + disty*disty)
                circle_grad[y][x] = dist

        # get it between -1 and 1
        max_grad = np.max(circle_grad)
        circle_grad = circle_grad / max_grad
        circle_grad -= 0.5
        circle_grad *= 2.0
        circle_grad = -circle_grad
        if self.show_the_process:
            Image.fromarray(self.prep_world(circle_grad)).show()

        world_noise = np.zeros_like(world)

        for i in range(self.shape[0]):
            for j in range(self.shape[1]):
                if circle_grad[i][j]>0:
                    world_noise[i][j] = (world[i][j] * circle_grad[i][j])
        if self.show_the_process:
            Image.fromarray(self.prep_world(world_noise)).show()

        terrain_colors = [self.color_dict["blue"], self.color_dict["beach"], self.color_dict["sandy"], 
                    self.color_dict["green"], self.color_dict["darkgreen"], self.color_dict["mountain"], 
                    self.color_dict["snow"]]

        maze_colors = [0,1,2,3,4,5,6] #this will be used as the maze.

        island_world_primer = self.prep_world(world_noise)
        shape = island_world_primer.shape
    
        island_world_primer = island_world_primer[self.slice_off:shape[0]-self.slice_off, self.slice_off:shape[1]-self.slice_off]
        island_world_primer= cv2.resize(island_world_primer,(self.final_rez_x,self.final_rez_y),fx=0, fy=0, interpolation = cv2.INTER_NEAREST)

        island_world_terrain = self.add_color2(island_world_primer, terrain_colors).astype(np.uint8)
        island_world_maze = self.add_color2(island_world_primer, maze_colors).astype(np.uint8)

        """
        # Set entrance and exit
        we scan the edges, and if the inside parallel square is available,
        we can set it as the start point.

        modify to truly random arrangement sans symmetry?
        """
        forbidden_start = [0,6] #cant start in water or on snow
        rand = np.random.randint(2)
        #rand = 1

        if rand == 0:#we start on the sides
            left_edge, right_edge = 0, self.final_rez_x-1 #outer limits.
            sample_list =[n for n in range(self.final_rez_y)]
            random.shuffle(sample_list)
            positions=[]
            terminate = False
            while not terminate: #select from the left
                for n in sample_list:
                    if (island_world_maze[n][left_edge] not in forbidden_start):
                        positions.append([n,left_edge])
                        terminate = True
                        break
                left_edge +=1 #didnt hit anything, move inwards.
            random.shuffle(sample_list)        
            terminate = False
            while not terminate: #select from the right
                for n in sample_list:
                    if (island_world_maze[n][right_edge] not in forbidden_start):
                        positions.append([n,right_edge])
                        terminate = True
                        break
                right_edge -=1 #didnt hit anything, move inwards.
            random.shuffle(positions) #randomize
            self.start, self.finish = positions[0], positions[1]


        elif rand == 1:#we start on the top/bottom
            top_edge, bottom_edge = 0, self.final_rez_y-1 #outer limits.
            sample_list =[n for n in range(self.final_rez_x)]
            random.shuffle(sample_list)
            positions=[]
            terminate = False
            while not terminate:
                for n in sample_list:
                    if (island_world_maze[top_edge][n] not in forbidden_start):
                        positions.append([top_edge,n])
                        terminate = True
                        break
                top_edge +=1 #didnt hit anything, move inwards.
            random.shuffle(sample_list)
            terminate = False
            while not terminate:
                for n in sample_list:
                    if (island_world_maze[bottom_edge][n] not in forbidden_start):
                        positions.append([bottom_edge,n])
                        terminate = True
                        break
                bottom_edge -=1 #didnt hit anything, move inwards.
            random.shuffle(positions) #randomize
            self.start, self.finish = positions[0], positions[1]

        island_world_terrain[self.finish[0]][self.finish[1]] = self.color_dict["red"]
        #Image.fromarray(island_world_grad,'RGB').show()
        return island_world_terrain, island_world_maze, self.start, self.finish


def main():
        generator = Terrain_Generator(100,100)
        island_world_terrain, island_world_maze, start, finish = generator.generator()
        print(start, finish)
        plt.imshow(island_world_terrain)
        plt.show()

if __name__ == "__main__":
       main()