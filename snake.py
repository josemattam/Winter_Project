# -*- coding: utf-8 -*-
"""
Created on Sun Dec 13 18:37:19 2020

Author: spideyonthego
"""

import numpy as np

board_size = 10
state = np.zeros((board_size, board_size))

# returns the next state matrix given the current state and move
def move_state(move):
    return None


# put walls in the matrix (5)
state[:, 0] = 5 
state[0, :] = 5
state[-1, :] = 5
state[:, -1] = 5

# spawn snake (1)
state[-2, [1, 2, 3]] = 1

# spawn food block (2)
choices = np.where(state==0)
x_food = np.random.choice(choices[0])
y_food = np.random.choice(choices[1])
state[x_food, y_food] = 2

print(state)

"""
while running:
    # input to network 
    # ...
    # get output (W, A, S, D) into variable move
    
    # for example
    move = W
    
    cand_state = move_state(state, move)
    if check_valid(cand_state):
        # check if it has eaten food and if it has, reward
        state = cand_state
    else:
        # do if snake runs into itself, wall, or tries to go back into itself
        
"""