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
    
    # block array list
    block_list: []

        
        