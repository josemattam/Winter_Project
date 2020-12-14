from dataclasses import dataclass
import random
import pygame
import tkinder as tk

@dataclass
class block():
    
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
class snake():
    
    # head location
    head_x: int
    head_y: int 
    
    # array list of snake blocks
    snake_blocks: []
    
    # snake length
    length: int
    
    # length of the square grid map
    grid_length: int
    
    # direction the snake is facing
    direction: str
    
    
    # constructor: will create the snake and add it to the world map
    # requirements: either no parameters or all included parameters
    def __init__(self, head_x = 3, head_y = 8, grid_length = 10):
        
        
        create_snake()
        
        pass
    
    
    # adds the snake to the grid, sets the direction the snake faces
    # TODO: make the body spawn in a random direction
    def create_snake(self):
        
        # add the head to the snake_block list
        snake_blocks.append(block(head_x, head_y, 1))
        
        # sets the body at the bottom left location of the grid
        snake_blocks.append(block(head_x - 1, head_y, 1))
        snake_blocks.append(block(head_x - 2, head_y, 1))

        direction = "east"
        return
    
    
    #def snake_move(self, new_dir):
        
        
        
    
"""        
    # returns the list of snake blocks
    def get_snake_blocks(self):
        return snake_blocks
"""

    
        
    

        
        