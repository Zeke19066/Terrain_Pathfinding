'''
We generate the maze and feed it to the search_ai

At each tick, we plot the closed list;
once the finishline is found we flash the finl path in a different color.

Everything is generated and stored, to be rendered by the game in the loop.


EVERYTHING IN Y,X FORMAT

'''
import pygame
import numpy as np
import time
import os
import random
from collections import deque

import Terrain_AI
import Terrain_Generator

class SnakeGame():
    def __init__(self):
        print('Game Initialized!')
        self.ai_control = True #no human control.
        self.random_mode = True
        self.death_count = 0 #how many ded snek?

        self.res_x = 200#48
        self.res_y = 100#27
        self.pixel_size = 8
        self.game_speed = 6500
        self.final_speed = 0
        self.game_close = False

        self.modes = ["Squared Difference", "Geometric Mean", "Manhattan Heuristic"]
        self.py_ai = Terrain_AI.Terrain_AI(f_mode=2) #dont forget fmode
        self.maze_generator = Terrain_Generator.Terrain_Generator(self.res_y,self.res_x)
        self.cycle = 1
        self.loop_setup = True
        self.relay_count, self.relay_limit, self.relay_bool = 0 , 5, False

        os.environ['SDL_VIDEO_WINDOW_POS'] = f"{25},{25}" # This is how we set the window position on the screen. Must come before pygame init.
        
        pygame.init()
        self.dis = pygame.display.set_mode((self.res_x*self.pixel_size, self.res_y*self.pixel_size))
        #self.dis = pygame.display.set_mode((self.res_x*self.pixel_size, self.res_y*self.pixel_size), pygame.FULLSCREEN)
        pygame.display.set_caption('Maze v1')

        self.screen = pygame.Surface((self.res_x, self.res_y), pygame.SRCALPHA)
        self.blank_screen = self.screen.copy()
        self.terrain_surface = pygame.Surface((self.res_x, self.res_y))
        self.clock = pygame.time.Clock()
        self.font_style = pygame.font.SysFont("bahnschrift", 10)
        self.score_font = pygame.font.SysFont("consolas", 10)

        self.color_dict={
            "white": (255, 255, 255),
            "yellow": (255, 240, 31), #(255, 255, 102),
            "orange": (255,165,0),#(255, 200, 50),
            "purple": (102, 0, 204),
            "pink": (255, 16, 240),
            "black": (0, 0, 0),
            "soft_red": (213, 50, 80),
            "red":(255,0,0),
            "green": (0, 255, 0),
            "soft_blue": (50, 153, 213),
            "blue": (0,0,255),
            "gray": (150,150,150),
            "light_gray": (200,200,200),
            "transparent": (150,150,150, 0),
            }
        self.open_color = self.color_dict["light_gray"]

    def score_generator(self, score):
        value = self.score_font.render("Your Score: " + str(score), True, self.color_dict["white"])
        self.screen.blit(value, [0, 0]) # Draw the score onto the screen at these coordinates.

    def path_plotter(self, path, finish_bool, relay_bool=False):
        path_color = self.path_colors[0]
        if finish_bool:
            path_color = self.path_colors[1]

        #If new terrain, draw to surface.
        if self.loop_setup:
            for y in range(self.res_y):
                for x in range(self.res_x):
                    cell_color = self.terrain_map[y][x]
                    pygame.draw.rect(self.terrain_surface, cell_color, [x, y, 1, 1])

        if relay_bool or self.loop_setup: #now working without "True"
            self.screen = self.blank_screen.copy()

        for pixel in path:
            pygame.draw.rect(self.screen, path_color, [pixel[1], pixel[0], 1, 1])

        self.screen.set_alpha(150)
        self.dis.blit(pygame.transform.scale(self.terrain_surface, self.dis.get_rect().size), (0, 0))
        self.dis.blit(pygame.transform.scale(self.screen, self.dis.get_rect().size), (0, 0), special_flags=(pygame.BLEND_RGBA_ADD))
        pygame.display.update()

    def message(self, msg, color):
        mesg = self.font_style.render(msg, True, color)
        #self.screen.blit(mesg, [int(self.res_x / 6), int(self.res_y / 3)])
        self.screen.blit(mesg, [0, int(self.res_y / 3)])

    def gameLoop(self):
        if self.loop_setup:
            #setup the start of each game:
            self.path_colors = [self.color_dict["green"],self.color_dict["soft_blue"],self.color_dict["orange"], 
                        self.color_dict["purple"], self.color_dict["pink"], self.color_dict["yellow"]]
            self.terrain_map, self.maze_map, self.start, self.finish = self.maze_generator.generator()
            self.path_plotter([], False)
            self.loop_setup = False

        #rand = np.random.randint(3)
        rand = 1
        self.py_ai.f_mode = rand #change the search mode randomly
        pygame.display.set_caption(f'Maze v1   f-Mode: {self.modes[rand]}   Relay: {self.relay_count}/{self.relay_limit}')
        random.shuffle(self.path_colors)
        self.game_close, terminal_bool = False, False

        #Main game loop
        for path_list, finish_bool, self.relay_bool in self.py_ai.astar_path(self.maze_map, self.start, self.finish):

            #First process user quit command if preset.
            for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        terminal_bool = True
                        pygame.quit()
                        quit()
                        return terminal_bool
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            print('Exiting Now')
                            terminal_bool = True
                            pygame.quit()
                            quit()
                            return terminal_bool

            if self.relay_bool:
                self.path_plotter(path_list, finish_bool, True)
                time.sleep(1.5)
                self.relay_count+=1
                print(self.relay_count)
                if self.relay_count > self.relay_limit:
                    self.relay_count = 0
                    self.game_close = True
                    break
                self.start = path_list[-1]
                self.gameLoop()
                self.game_close = True
                break

            #now run the AI stuff
            self.path_plotter(path_list, finish_bool)

            if finish_bool:
                self.game_close = True
                break

            self.clock.tick(self.game_speed)
            self.cycle += 1
            #pygame.image.save(self.dis,"screenshot.png")

        self.loop_setup = True
        # Exit Sequence
        if self.game_close == True:
            while self.game_close == True:
                if self.ai_control:
                    return terminal_bool

                for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            terminal_bool = True
                            return terminal_bool
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_ESCAPE:
                                print('Exiting Now')
                                terminal_bool = True
                                return terminal_bool
        

        pygame.quit()
        quit()

    def color_generator(self):
        return (np.random.randint(0,256),np.random.randint(0,256),np.random.randint(0,256))


def main():
    snek = SnakeGame()
    while 1:
        snek.gameLoop()

if __name__ == "__main__":
    main()