"""
Created on Sun Dec 13 18:37:19 2020

Author: Jose Mattam and Anand Krishnakumar
"""
from dataclasses import dataclass
import random
import pygame
import tkinder as tk
import numpy as np
from collections import deque


@dataclass
class Block():
    
    # x and y coordinates:
    xloc: int
    yloc: int
    
    # type of block:
    #   1:- snake
    #   0:- empty
    #   2:- food block
    #   5:- wall
    block_type: int
    
    def __init__(self, _xloc, _yloc, _block_type):
        self.xloc = _xloc
        self.yloc = _yloc
        self.block_type = _block_type

    
@dataclass
class Snake():
    
    # head location
    head_x: int
    head_y: int 
    
    # array list of snake blocks
    snake_blocks: deque[Block]
        
    # length of the square grid map
    grid_length: int
    
    # direction the snake is facing
    direction: str
    
    # snake length
    length: int
    
    # adds the snake to the grid, sets the direction the snake faces
    # TODO: make the body spawn in a random direction
    def __create_snake(self):
        
        # not sure if we need to initialize snake_blocks
        
        # add the head to the snake_block list
        self.snake_blocks.append(Block(self.head_x, self.head_y, 1))
        
        # sets the body at the bottom left location of the grid
        self.snake_blocks.append(Block(self.head_x - 1, self.head_y, 1))
        self.snake_blocks.append(Block(self.head_x - 2, self.head_y, 1))

        self.length = 3
        return
    
    # constructor: will create the snake and add it to the world map
    # requirements: either no parameters or all included parameters
    def __init__(self, head_x = 3, head_y = 8, grid_length = 10, direction = "east"):
        self.head_x = head_x
        self.head_y = head_y
        self.direction = direction
        self.grid_length = grid_length
        self.direction = direction
        self.create_snake()
        
        return
    
    # adds a new head to the snake
    def add_head_xy(self, x, y):
        self.head_x = x
        self.head_y = y
        
        # add new snake head block
        new_block = Block(x, y, 1)
        self.snake_blocks.append(new_block)
        return
        
    # removes the tail end of the snake and returns that block
    def remove_tail(self):        
        return self.snake_blocks.pop()
    
    
    #def snake_move(self, new_dir):
        
        
        
@dataclass
class World():
    
    # length of the square grid map
    grid_length: int
       
    # world grid
    world_grid: [int][int]
    
    # the player's snake
    snake: Snake
    
    # the player's food_count
    food_count: int
    
    def __init__(self, grid_length = 10):
        self.grid_length = grid_length
        
        # initialize the world grid to a 2d array of zeroes
        self.world_grid = np.zeros((grid_length, grid_length))
        
        # set the walls in the world grid
        self.world_grid[:, 0] = 5 
        self.world_grid[0, :] = 5
        self.world_grid[-1, :] = 5
        self.world_grid[:, -1] = 5
    
        self.food_count = 0
        
        # initialize the snake
        self.snake()
        return
    
    # move the snake in a new or same direction based on the input direction given    
    # returns 1 if movement was successful and 0 if not (ie. if the snake hits a wall/itself or not)
    def move_snake(self, _direction):
        
        # if the given direction is the same as the current direction,
        # then move in the same direction
        if (self.snake.direction == _direction):
            return self.move(self.snake.direction)           
            
        # if the given direction is the opposite direction the snake faces,
        # then move in the same direction the snake was moving
        elif ((self.snake.direction == "north" and _direction == "south" ) or
              (self.snake.direction == "south" and _direction == "north") or
              (self.snake.direction == "east" and _direction == "west") or
              (self.snake.direction == "west" and _direction == "east")):
            return self.move(self.snake.direction)

        else:
            # move in the valid new direction
            return self.move(_direction)


    # private helper function that moves the snake in the grid and sets its new direction
    def __move(self, _direction):

        # step 1: move head
        
        # change in x and y coords
        dx = 0
        dy = 0
        
        if _direction == "north":
            dy = 1
            
        elif _direction == "south":
            dy = -1
        
        elif _direction == "east":
            dx = 1
        
        else:
            dx = -1
         
        new_x = self.snake.head_x + dx   
        new_y = self.snake.head_y + dy
         
        # check if the snake hits the wall or itself
        if self.world_grid[new_x][new_y] == 5 or self.world_grid[new_x][new_y] == 1:
            return 0
                          
        # implement change to world grid
        self.world_grid[new_x][new_y] = 1   
           
        
        # step 2: move tail
        
        # remove the tail end of the snake
        tail_block = self.snake.remove_tail()
        
        # implement change to world grid
        self.world_grid[tail_block.xloc][tail_block.yloc] = 0
        
        # successful move
        return 1
    
    #add to the snake length when it eats
    
"""        
    # returns the list of snake blocks
    def get_snake_blocks(self):
        return snake_blocks
"""

    
        
    

        
        