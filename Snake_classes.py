"""
Created on Sun Dec 13 18:37:19 2020

Author: Jose Mattam and Anand Krishnakumar
"""
from dataclasses import dataclass
import random
import pygame
import tkinder as tk
from tkinder import messagebox
import numpy as np
from collections import deque


# ADD POSSIBLE REWARD SYSTEM TYPES 

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
        
    ## VIEW FUNCTION ##
        
    def draw_block(self, width, rows, surface):
        color = (0, 0, 0)
        
        # if it's a snake block
        if self.block_type == 1:
            color = (255, 255, 255)
            
        # if it's a wall block
        elif self.block_type == 5:
            color = (255, 0, 0)
            
        # if it's a food block
        elif self.block_type == 2:
            color = (0, 0, 255)
            
        distance = width // rows
        
        pygame.draw.rect(surface, color, (self.xloc * distance + 1, self.yloc * distance + 1,
                                          distance - 2, distance - 2))

    
@dataclass
class Snake():
    
    # head location
    head_x: int
    head_y: int 
    
    # array list of snake blocks
    snake_blocks: deque[Block]
        
    # length of the square grid map
    grid_rows: int
    
    # direction the snake is facing
    direction: str
    
    # snake length
    length: int
    
    # constructor: will create the snake and add it to the world map
    # requirements: either no parameters or all included parameters
    def __init__(self, head_x = 3, head_y = 18, grid_rows = 20, direction = "east"):
        self.head_x = head_x
        self.head_y = head_y
        self.direction = direction
        self.grid_rows = grid_rows
        self.direction = direction
        self.create_snake()
        
        return
    
    # adds the snake to the grid, sets the direction the snake faces
    # TODO: make the body spawn in a random direction
    def __create_snake(self):
        
        # not sure if we need to initialize snake_blocks
        
        # add the head to the snake_block list
        self.snake_blocks.append(Block(self.head_x, self.head_y, 1))
        
        
        # In the future, world will randomly select the dir and blocks, change params to accept the blocks
        # sets the body at the bottom left location of the grid
        self.snake_blocks.append(Block(self.head_x - 1, self.head_y, 1))
        self.snake_blocks.append(Block(self.head_x - 2, self.head_y, 1))

        self.length = 3
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
    
    def get_head(self):
        return Block(self.head_x, self.head_y, 1)
    
    def get_tail(self):
        return Block(self.snake_blocks[-1].head_x, self.snake_blocks[-1].head_y, 1)
    
    ## VIEW FUNCTION ##
    def draw_snake(self, width, rows, surface):
        for block in self.snake_blocks:
            block.draw_block(width, rows, surface)
            
    
        
        
        
        
@dataclass
class World():
    
    ## IMPLEMENT REWARD SYSTEMS
    
    # length of the square grid map
    grid_rows: int
    
    # length of the side of the program window
    prog_length: int
    

       
    # world grid
    world_grid: [int][int]
    
    # the player's snake
    snake: Snake
    
    # the food block
    food: Block
    
    # the walls as an array of blocks
    walls: [Block]
    
    # the player's food_count
    food_count: int
    
    # the player's score
    score: int
    """
    """
    
    def __init__(self, grid_rows = 20, prog_length = 500):
        self.grid_rows = grid_rows
        self.prog_length = prog_length
        self.score = 0
        self.food_count = 0
        
        # VIEW: set up the program window to draw onto
        self.prog_window = pygame.display.set_mode((self.prog_length, self.prog_length))

        
        # initialize the world grid to a 2d array of zeroes
        self.world_grid = np.zeros((grid_rows, grid_rows))
        
        self.set_walls()
        
        self.spawn_snake()
        
        self.spawn_food()
        
        #start clock...
        
        return
    
    
    # set the walls in the world
    #shaky
    def set_walls(self):
        self.world_grid[:, 0] = 5 
        self.world_grid[0, :] = 5
        self.world_grid[-1, :] = 5
        self.world_grid[:, -1] = 5
        
        i = 0
        while i < self.world_grid[:, 0]:
            self.walls.append(Block(i, 0, 5))
            
        i = 0
        while i < self.world_grid[0, :]:
            self.walls.append(Block(0, i, 5))
            
        i = 0
        while i < self.world_grid[-1, :]:
            self.walls.append(Block(self.grid_rows - 1, i, 5))
            
        i = 0
        while i < self.world_grid[:, -1]:
            self.walls.append(Block(i, self.grid_rows - 1, 5))
        
        
    
    # move the snake in a new or same direction based on the input direction given    
    # returns 1 if movement was successful and 0 if not (ie. if the snake hits a wall/itself or not)
    def snake_move(self, _direction):
        
        # if the given direction is the same as the current direction,
        # then move in the same direction
        if (self.snake.direction == _direction):
            return self.move_action(self.snake.direction)           
            
        # if the given direction is the opposite direction the snake faces,
        # then move in the same direction the snake was moving
        elif ((self.snake.direction == "north" and _direction == "south" ) or
              (self.snake.direction == "south" and _direction == "north") or
              (self.snake.direction == "east" and _direction == "west") or
              (self.snake.direction == "west" and _direction == "east")):
            # reducing score to discouage this
            self.score -= 5
            return self.move_action(self.snake.direction)

        else:
            # move in the valid new direction
            self.snake.direction = _direction
            return self.move_action(_direction)


    # private helper function that moves the snake in the grid and sets its new direction.
    # performs suitable action if the snake interacts with another block
    def __move_action(self, _direction):

        # list of all changed blocks (for use in change of view)
        changed_blocks = []
        changed_blocks.append(self.snake.get_head())
        changed_blocks.append(self.snake.get_tail())        

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

        # implement change to world grid and to the snake
        self.world_grid[new_x][new_y] = 1   
        self.snake.add_head_xy(new_x, new_y)
        changed_blocks.append(self.snake.get_head())

           
        # if the snake hits a food block
        if self.world_grid[new_x][new_y] == 2:
            self.change_view_list(changed_blocks)
            return self.snake_eat(_direction)
        
        
        # step 2: move tail
        
        # remove the tail end of the snake
        tail_block = self.snake.remove_tail()
        
        # implement change to world grid
        self.world_grid[tail_block.xloc][tail_block.yloc] = 0
        changed_blocks.append(self.snake.get_tail())

        self.change_view_list(changed_blocks)
        # successful move
        return 1
    
    
    # increases snake length and spwans another food
    def __snake_eat(self, _direction):        
        # add to the snake length when it eats
        self.snake.length += 1
        self.score += 10
        
        # TODO: ADD TO SCORE, add chang to grid view change
        self.spawn_food()

    # spawn the snake
    def spawn_snake(self): 
        
        #
        self.snake = Snake()
        # randomize later
        self.world_grid[3][18] = 1
        self.world_grid[2][18] = 1
        self.world_grid[1][18] = 1
        return Block(self.snake.head_x, self.snake.head_y, 1)
        
    # spawns the food in a random valid position    
    def spawn_food(self):
        choices = np.where(self.world_grid == 0)
        x_food = np.random.choice(choices[0])
        y_food = np.random.choice(choices[1])
        self.world_grid[x_food, y_food] = 2
        self.food = Block(x_food, y_food, 2)
        self.change_view(self.food)
        return 
    
    # resets the game (controller and view)
    def reset(self):
        # snake:
        self.snake = Snake()
        self.spawn_snake()  
        # food:
        self.spawn_food()
        # walls:
        self.set_walls()
        # view:
        self.setup_view()
        
    
    ## VIEW FUNCTIONS ##
        
    # calls the necessary functions to setup the view of a game of snake
    def setup_view(self):
        # set the bg to be black
        self.prog_window.fill((0, 0, 0))
        self.draw_grid()
        # draw walls
        self.change_view_list(self.walls)
        # draw snake
        self.change_view_list(self.snake.snake_blocks)     
        # draw food
        self.change_view(self.food)            

    # draws the grid on which the snake moves and plays the game
    def draw_grid(self):
        distance = self.prog_length // self.grid_rows
        x = 0
        y = 0
        for row in range(self.grid_rows):
            x += distance
            y += distance
            
            pygame.draw.line(self.prog_window, (255,255,255), (x, 0), (x, self.prog_length))
            pygame.draw.line(self.prog_window, (255,255,255), (0, y),(self.prog_length, y))
    
    
    # draws the given changed block. Needed for the updation of the game for each frame
    def change_view(self, block):
        # block color = black
        color = (0, 0, 0)
        
        # if the block is a snake
        if block.block_type == 1:
            color = (255, 255, 255)
        
        # if the block is a food block
        elif block.block_type == 2:
            color = (0, 0, 255)
            
        # if the block is a wall
        elif block.block_type == 5:
            color = (255, 0, 0)
            
            
        # TODO COMMENT EXPLAINING
        distance = self.prog_length // self.grid_rows
            
        pygame.draw.rect(self.prog_window, color, (block.head_x * distance + 1,
                                                   block.head_y * distance + 1,
                                                   distance - 2, distance - 2))
        
        
    
    # change view for a list of blocks
    def change_view_list(self, blocks):
        for block in blocks:
            self.change_view(block)

    
    # displays the end message. called when a game is over
    def end_message(self):
        # press any key to continue?
        # check how iterations are carried out
        
        root = tk.Tk()
        root.attributes("-topmost", True)
        root.withdraw()
        messagebox.showinfo("Game Over", "Score: " + self.score)
        try:
            root.destroy()
        except:
            pass
            
    
    ## END OF VIEW FUNCTIONS ##
    
    
    ## CONTROLLER FUNCTIONS ##
    
    # controller function for all key/mouse events
    def keypress_event(self):
        # for every key/mouse press event, iterate this loop
        for event in pygame.event.get():
            
            # if the red close 'x' is clicked then quit
            if event.type == pygame.QUIT:
                pygame.quit()
                
            # list of the pressed keys
            keys = pygame.key.get_pressed()
            
            for key in keys:
                if keys[pygame.K_W]:
                    self.snake_move("north")
                    
                elif keys[pygame.K_S]:
                    self.snake_move("south")
                    
                elif keys[pygame.K_A]:
                    self.snake_move("west")
                    
                elif keys[pygame.K_D]:
                    self.snake_move("east")
                    
                    
    
                
    ## END OF CONTROLLER FUNCTIONS ##                
                
                
    
def main():
        
    # create a game world
    world = World()
        
    # VIEW: create the program display window
    window = pygame.display.set_mode((world.prog_length, world.prog_length))
    
    #
    clock = pygame.time.Clock()
        
    while True:
        # 
        pygame.time.delay(50)
        clock.tick(10)
    
        # checks for input and does accordingly. valid = 1 the game continues
        valid = world.keypress_event()
        
        # if the game ends
        if valid == 0:
            world.end_message()
            world.reset()
            break
            
        world.draw_window(window)
            
    return
    
    
main()
        
            
        
        
        
        

    
        
    

        
        