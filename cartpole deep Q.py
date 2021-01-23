import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

"""Custom game I created to experiment with stuff"""
# Environment
#          1
#        4 0 2
#          3

# food blob is spawned randomly at locations 1, 2, 3, or 4
# agent blob is spawned randomly at location 0
# agent should move to food location

# States
# 1: food is at 1
# 2: food is at 2
# 3: food is at 3
# 4: food is at 4

class Blob:
    def __init__(self, loc=False):
        if not loc:
            self.loc = np.random.choice([1, 2, 3, 4])
        else:
            self.loc = loc
    
    def move(self, to_loc, food):
        self.loc = to_loc
        if self.loc == food.loc:
            return 1 # won
        else:
            return -1

# Q-table
Q = np.random.rand(4, 4)
Q_initial = np.copy(Q)

epsilon = 0.5 # exploration factor

def play_bot(Qtable, state):
    u = np.random.uniform()
    if u > epsilon:
        action = np.argmax(Qtable[state - 1]) + 1
    else:
        action = np.random.choice([1, 2, 3, 4])
    return action

alpha = 0.5 # learning rate
niter = 200 # number of episodes

epsilon_reduction_rate = epsilon/niter
for episode in range(niter):
    Agent = Blob(0)
    Food = Blob()
    state = Food.loc
    action = play_bot(Q, state)
    won = Agent.move(action, Food)
    # print(won)
    curr_Q = Q[Food.loc - 1, action - 1]
    Q[Food.loc - 1, action - 1] = curr_Q + alpha*(won - curr_Q)
    epsilon -= epsilon_reduction_rate
    
    
    
N_ACTIONS = 4
# initialise Q-network
# inputs are state information for arbitrarily many states
# state information is locations of food blob and agent blob
QN = keras.models.Sequential()
QN.add(keras.Input(shape=(1,)))
QN.add(keras.layers.Dense(N_ACTIONS, activation='relu'))
QN.compile(optimizer=keras.optimizers.RMSprop(learning_rate=0.2),
              loss=keras.losses.CategoricalCrossentropy())

# initialise Target-network
TN = tf.keras.models.clone_model(QN)
TN.set_weights(QN.get_weights())

train_X = np.empty((100, 1))
train_Y = np.empty((100, N_ACTIONS))

# an new agent function that works with NNS
epsilon = 0.5 # exploration factor
def play_botNN(Qvals):
    # gets the Qvals of actions at a specific state
    # returns random action with probability epsilon
    # returns best action with probability 1-epsilon
    u = np.random.uniform()
    if u > epsilon:
        action = np.argmax(Qvals[0]) + 1
    else:
        action = np.random.choice([1, 2, 3, 4])
    return action
    
curr_state_memory = []
action_memory = []
reward_memory = []
MEM_RESET = 0
for episode in range(100):
    Agent = Blob(0)
    Food = Blob()
    state = Food.loc
    NN_input = np.array([state]).reshape(1, 1)
    Qs = QN.predict(NN_input)
    action = play_botNN(Qs)
    won = Agent.move(action, Food)
    
    # FIT QN
    # step 1: retrieve y-label 
    # (no need for TN in our case as there is only one move)
    output = won
    train_X[episode] = state
    y_Qs = -1 * np.ones(N_ACTIONS)
    y_Qs[state-1] = 1
    train_Y[episode] = y_Qs
    # print(state, y_Qs)

QN.fit(train_X, train_Y)