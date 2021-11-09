# Maze generator -- Randomized Prim Algorithm

## Imports
import random
import numpy as np
import time
from colorama import init
from colorama import Fore, Back, Style
import matplotlib.pyplot as plt


#plot_maze = np.rot90(plot_maze, 2) #rotate by 180deg
#plot_maze = np.fliplr(plot_maze) #flip horizontally

class Maze_Generator():
	
	def __init__(self, height, width):
		## Main code
		# Init variables
		self.wall_symbol = 'w'
		self.cell = 'c'
		self.unvisited = 'u'
		self.height = height
		self.width = width
		self.maze = []


	# Find number of surrounding cells
	def surroundingCells(self, rand_waall):
		s_cells = 0
		if (self.maze[rand_waall[0]-1][rand_waall[1]] == 'c'):
			s_cells += 1
		if (self.maze[rand_waall[0]+1][rand_waall[1]] == 'c'):
			s_cells += 1
		if (self.maze[rand_waall[0]][rand_waall[1]-1] == 'c'):
			s_cells +=1
		if (self.maze[rand_waall[0]][rand_waall[1]+1] == 'c'):
			s_cells += 1

		return s_cells


	def generator(self):
		self.maze = []

		# Denote all cells as unvisited
		for i in range(0, self.height):
			line = []
			for j in range(0, self.width):
				line.append(self.unvisited)
			self.maze.append(line)

		# Randomize starting point and set it a cell
		starting_height = int(random.random()*self.height)
		starting_width = int(random.random()*self.width)
		if (starting_height == 0):
			starting_height += 1
		if (starting_height == self.height-1):
			starting_height -= 1
		if (starting_width == 0):
			starting_width += 1
		if (starting_width == self.width-1):
			starting_width -= 1

		# Mark it as cell and add surrounding waals to the list
		self.maze[starting_height][starting_width] = self.cell
		waals = []
		waals.append([starting_height - 1, starting_width])
		waals.append([starting_height, starting_width - 1])
		waals.append([starting_height, starting_width + 1])
		waals.append([starting_height + 1, starting_width])

		# Denote waals in maze
		self.maze[starting_height-1][starting_width] = 'w'
		self.maze[starting_height][starting_width - 1] = 'w'
		self.maze[starting_height][starting_width + 1] = 'w'
		self.maze[starting_height + 1][starting_width] = 'w'

		while (waals):
			# Pick a random wall
			rand_waall = waals[int(random.random()*len(waals))-1]

			# Check if it is a left wall
			if (rand_waall[1] != 0):
				if (self.maze[rand_waall[0]][rand_waall[1]-1] == 'u' and self.maze[rand_waall[0]][rand_waall[1]+1] == 'c'):
					# Find the number of surrounding cells
					s_cells = self.surroundingCells(rand_waall)

					if (s_cells < 2):
						# Denote the new path
						self.maze[rand_waall[0]][rand_waall[1]] = 'c'

						# Mark the new waals
						# Upper cell
						if (rand_waall[0] != 0):
							if (self.maze[rand_waall[0]-1][rand_waall[1]] != 'c'):
								self.maze[rand_waall[0]-1][rand_waall[1]] = 'w'
							if ([rand_waall[0]-1, rand_waall[1]] not in waals):
								waals.append([rand_waall[0]-1, rand_waall[1]])


						# Bottom cell
						if (rand_waall[0] != self.height-1):
							if (self.maze[rand_waall[0]+1][rand_waall[1]] != 'c'):
								self.maze[rand_waall[0]+1][rand_waall[1]] = 'w'
							if ([rand_waall[0]+1, rand_waall[1]] not in waals):
								waals.append([rand_waall[0]+1, rand_waall[1]])

						# Leftmost cell
						if (rand_waall[1] != 0):	
							if (self.maze[rand_waall[0]][rand_waall[1]-1] != 'c'):
								self.maze[rand_waall[0]][rand_waall[1]-1] = 'w'
							if ([rand_waall[0], rand_waall[1]-1] not in waals):
								waals.append([rand_waall[0], rand_waall[1]-1])
					

					# Delete wall
					for wall in waals:
						if (wall[0] == rand_waall[0] and wall[1] == rand_waall[1]):
							waals.remove(wall)

					continue

			# Check if it is an upper wall
			if (rand_waall[0] != 0):
				if (self.maze[rand_waall[0]-1][rand_waall[1]] == 'u' and self.maze[rand_waall[0]+1][rand_waall[1]] == 'c'):

					s_cells = self.surroundingCells(rand_waall)
					if (s_cells < 2):
						# Denote the new path
						self.maze[rand_waall[0]][rand_waall[1]] = 'c'

						# Mark the new waals
						# Upper cell
						if (rand_waall[0] != 0):
							if (self.maze[rand_waall[0]-1][rand_waall[1]] != 'c'):
								self.maze[rand_waall[0]-1][rand_waall[1]] = 'w'
							if ([rand_waall[0]-1, rand_waall[1]] not in waals):
								waals.append([rand_waall[0]-1, rand_waall[1]])

						# Leftmost cell
						if (rand_waall[1] != 0):
							if (self.maze[rand_waall[0]][rand_waall[1]-1] != 'c'):
								self.maze[rand_waall[0]][rand_waall[1]-1] = 'w'
							if ([rand_waall[0], rand_waall[1]-1] not in waals):
								waals.append([rand_waall[0], rand_waall[1]-1])

						# Rightmost cell
						if (rand_waall[1] != self.width-1):
							if (self.maze[rand_waall[0]][rand_waall[1]+1] != 'c'):
								self.maze[rand_waall[0]][rand_waall[1]+1] = 'w'
							if ([rand_waall[0], rand_waall[1]+1] not in waals):
								waals.append([rand_waall[0], rand_waall[1]+1])

					# Delete wall
					for wall in waals:
						if (wall[0] == rand_waall[0] and wall[1] == rand_waall[1]):
							waals.remove(wall)

					continue

			# Check the bottom wall
			if (rand_waall[0] != self.height-1):
				if (self.maze[rand_waall[0]+1][rand_waall[1]] == 'u' and self.maze[rand_waall[0]-1][rand_waall[1]] == 'c'):

					s_cells = self.surroundingCells(rand_waall)
					if (s_cells < 2):
						# Denote the new path
						self.maze[rand_waall[0]][rand_waall[1]] = 'c'

						# Mark the new waals
						if (rand_waall[0] != self.height-1):
							if (self.maze[rand_waall[0]+1][rand_waall[1]] != 'c'):
								self.maze[rand_waall[0]+1][rand_waall[1]] = 'w'
							if ([rand_waall[0]+1, rand_waall[1]] not in waals):
								waals.append([rand_waall[0]+1, rand_waall[1]])
						if (rand_waall[1] != 0):
							if (self.maze[rand_waall[0]][rand_waall[1]-1] != 'c'):
								self.maze[rand_waall[0]][rand_waall[1]-1] = 'w'
							if ([rand_waall[0], rand_waall[1]-1] not in waals):
								waals.append([rand_waall[0], rand_waall[1]-1])
						if (rand_waall[1] != self.width-1):
							if (self.maze[rand_waall[0]][rand_waall[1]+1] != 'c'):
								self.maze[rand_waall[0]][rand_waall[1]+1] = 'w'
							if ([rand_waall[0], rand_waall[1]+1] not in waals):
								waals.append([rand_waall[0], rand_waall[1]+1])

					# Delete wall
					for wall in waals:
						if (wall[0] == rand_waall[0] and wall[1] == rand_waall[1]):
							waals.remove(wall)


					continue

			# Check the right wall
			if (rand_waall[1] != self.width-1):
				if (self.maze[rand_waall[0]][rand_waall[1]+1] == 'u' and self.maze[rand_waall[0]][rand_waall[1]-1] == 'c'):

					s_cells = self.surroundingCells(rand_waall)
					if (s_cells < 2):
						# Denote the new path
						self.maze[rand_waall[0]][rand_waall[1]] = 'c'

						# Mark the new waals
						if (rand_waall[1] != self.width-1):
							if (self.maze[rand_waall[0]][rand_waall[1]+1] != 'c'):
								self.maze[rand_waall[0]][rand_waall[1]+1] = 'w'
							if ([rand_waall[0], rand_waall[1]+1] not in waals):
								waals.append([rand_waall[0], rand_waall[1]+1])
						if (rand_waall[0] != self.height-1):
							if (self.maze[rand_waall[0]+1][rand_waall[1]] != 'c'):
								self.maze[rand_waall[0]+1][rand_waall[1]] = 'w'
							if ([rand_waall[0]+1, rand_waall[1]] not in waals):
								waals.append([rand_waall[0]+1, rand_waall[1]])
						if (rand_waall[0] != 0):	
							if (self.maze[rand_waall[0]-1][rand_waall[1]] != 'c'):
								self.maze[rand_waall[0]-1][rand_waall[1]] = 'w'
							if ([rand_waall[0]-1, rand_waall[1]] not in waals):
								waals.append([rand_waall[0]-1, rand_waall[1]])

					# Delete wall
					for wall in waals:
						if (wall[0] == rand_waall[0] and wall[1] == rand_waall[1]):
							waals.remove(wall)

					continue

			# Delete the wall from the list anyway
			for wall in waals:
				if (wall[0] == rand_waall[0] and wall[1] == rand_waall[1]):
					waals.remove(wall)
			


		# Mark the remaining unvisited cells as waals
		for i in range(0, self.height):
			for j in range(0, self.width):
				if (self.maze[i][j] == 'u'):
					self.maze[i][j] = 'w'

		
	
		"""
		# Set entrance and exit
		we scan the edges, and if the inside parallel square is available,
		we can set it as the start point.

		modify to truly random arrangement sans symmetry?
		"""
		rand = np.random.randint(2)
		if rand == 0:#we start on the sides
			positions=[]
			while 1:
				i = np.random.randint(self.height)
				if (self.maze[i][1] == 'c'):
					self.maze[i][0] = 'c'
					positions.append([i,0])
					break
			while 1:
				i = np.random.randint(self.height)
				if (self.maze[i][self.width-2] == 'c'):
					self.maze[i][self.width-1] = 'c'
					positions.append([i, self.width-1])
					break
			random.shuffle(positions) #randomize
			self.start, self.finish = positions[0], positions[1]

		elif rand == 1:#we start on the top/bottom
			positions=[]
			while 1:
				i = np.random.randint(self.width)
				if (self.maze[1][i] == 'c'):
					self.maze[0][i] = 'c'
					positions.append([0,i])
					break
			while 1:
				i = np.random.randint(self.width)
				if (self.maze[self.height-2][i] == 'c'):
					self.maze[self.height-1][i] = 'c'
					positions.append([self.height-1,i])
					break
			random.shuffle(positions) #randomize
			self.start, self.finish = positions[0], positions[1]

		shape = np.shape(self.maze)
		plot_maze = np.zeros((shape[0],shape[1]), dtype= int)

		for y in range(shape[0]):
			for x in range(shape[1]):
				if self.maze[y][x] == 'w':
					plot_maze[y][x] = 1


		#plt.imshow(plot_maze, cmap='Greys')
		#plt.show()
		return plot_maze, self.start, self.finish

if __name__ == "__main__":
	maze_generator = Maze_Generator(27,48)
	maze_generator.generator()