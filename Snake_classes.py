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
    
    # constructor: will create the snake and add it to the world map
    # requirements: either no parameters or all included parameters
    def __init__(self, head_x = 3, head_y = 8, grid_length = 10, direction = "east"):
        
        
        create_snake()
        
        pass
    
    
    # adds the snake to the grid, sets the direction the snake faces
    # TODO: make the body spawn in a random direction
    def create_snake(self):
        
        # not sure if we need to initialize snake_blocks
        
        # add the head to the snake_block list
        snake_blocks.append(block(head_x, head_y, 1))
        
        # sets the body at the bottom left location of the grid
        snake_blocks.append(block(head_x - 1, head_y, 1))
        snake_blocks.append(block(head_x - 2, head_y, 1))

        direction = direction
        length = 3
        return
    
    
    #def snake_move(self, new_dir):
        
        
        
@dataclass
class World():
    
    # length of the square grid map
    grid_length: int
       
    # world grid
    world_grid: [int][int]
    
    # the player's snake
    snake: Snake
    
    def __init__(self, grid_length = 10):
        
        # initialize the world grid to a 2d array of zeroes
        world_grid = np.zeros((grid_length, grid_length))
        
        # initialze the snake
        snake()
        pass
    
    # move the snake in a new or same direction based on the input direction given    
    def move_snake(self, _direction):
        
        # if the given direction is the same as the current direction,
        # then move in the same direction
        if (snake.direction == _direction)
            move(snake.direction)           
            
        # if the given direction is the opposite direction the snake faces,
        # then move in the same direction the snake was moving
        else if (snake.direction == "north" && _direction == "south" ||
                 snake.direction == "south" && _direction == "north" ||
                 snake.direction == "east" && _direction == "west" ||
                 snake.direction == "west" && _direction =+ "east")
            move(snake.direction)

        else:
            # move in the valid new direction
            move(_direction)

        return  
        
    # private helper function that moves the snake in the grid and sets its new direction
    def __move(self, _direction):
        
        
        
        pass
    
    #add to the snake length when it eats
    
"""        
    # returns the list of snake blocks
    def get_snake_blocks(self):
        return snake_blocks
"""

    
        
    

        
        