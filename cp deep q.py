import gym
import numpy as np
import tensorflow as tf
from tensorflow import keras

"""Cartpole game (if unfamiliar, google openai gym cartpole); tried to implement Deep Q-learning...haven't worked so far"""

env = gym.make('CartPole-v1')
print("Env initialized")

print("Action Space: {}".format(env.action_space))
print("State Space: {}".format(env.observation_space))


class Bot:
    def __init__(self, env):
        self.env = env # bot's environment
        
        # initialise Neural Networks
        self.QN = self._agent((4,), 2)
        self.TN = self._agent((4,), 2)
        self.TN.set_weights(self.QN.get_weights())
        
        
        # initialise information
        self.obs = env.reset()
        self.next_obs = None # initial observation
        self.action = None
        self.reward = None
        
        # exploration factor
        self.epsilon = 0.5 # initial exploration factor
        self.epsilon_change = -0.001 # change in exploration factor each move
        pass
    
    def _agent(self, state_shape, n_action): # creates an agent Neural network
        learning_rate = 0.001
        init = tf.keras.initializers.HeUniform()
        model = keras.Sequential()
        model.add(keras.layers.Dense(24, input_shape=state_shape, activation='relu', kernel_initializer=init))
        model.add(keras.layers.Dense(12, activation='relu', kernel_initializer=init))
        model.add(keras.layers.Dense(n_action, activation='linear', kernel_initializer=init))
        model.compile(loss=tf.keras.losses.Huber(), optimizer=tf.keras.optimizers.Adam(lr=learning_rate))
        return model
    
    def _get_qs(self, NN, obs): # gets q-values for a certain observation
        return NN.predict(obs.reshape(1, obs.shape[0]))[0]
    
    def play(self, obs):
        self.obs = obs # save observation
        if np.random.uniform() <= self.epsilon:
            # random action
            action = self.env.action_space.sample()
            print("random action", action)
        else:
            # max q action
            qs = self._get_qs(self.QN, obs)
            action = np.argmax(qs) # action with max q-value
            print("chosen action", action)
        self.epsilon += self.epsilon_change
        return action
    
    def played(self, next_obs, action, reward): # store move consequence
        self.next_obs = next_obs # observation after choosing action
        self.action = action # action taken
        self.reward = reward # reward received
        # in the future this will be stored in a memory
    
    def train(self): # training
        # Step 1: get current q values from QN
        # Step 2: get max next obs q value from TN
        # Step 3: update q value of chosen action by Bellman equation
        # Step 3: train QN
        _lambda = 0.9 # weightage given to future rewards
        cq = self._get_qs(self.QN, self.obs)
        curr_qs = 1.0*cq # current q-values
        max_next_q = np.max(self._get_qs(self.TN, self.next_obs)) # max next obs q-values
        curr_qs[self.action] = self.reward + _lambda * max_next_q # update
        
        # formatting
        train_X = self.obs.reshape(1, self.obs.shape[0])
        train_Y = curr_qs.reshape((1, 2))
        print(self.action)
        print(cq, curr_qs)
        self.QN.fit(train_X, train_Y, batch_size=1) # train
        print("Trained succesfully")  
    
    def train_TN(self): # train target network
        self.TN.set_weights(self.QN.get_weights())
        print("TN trained")

bot = Bot(env)
print("\n\nBot initialized with weights")
print(bot.QN.get_weights()[-1])
print("\n\n")

# Initialise Counters
TRAIN_RESET = 4 # train every 4th move
N_TRAIN = 1
TN_RESET = 20 # train target network every 50th move
N_TN = 1

for i_episode in range(2):
    observation = env.reset()
    for t in range(10):
        # env.render()
        action = bot.play(observation) # get bot action
        observation, reward, done, _ = env.step(action)
        bot.played(observation, action, reward) # give bot information
        
        # counter stuff
        N_TRAIN += 1
        N_TN += 1
        if N_TRAIN % TRAIN_RESET == 0:
            bot.train()
            N_TRAIN = 1
        if N_TN % TN_RESET == 0:
            bot.train_TN() # train target network
            N_TN = 1
            
        # check if episode done
        if done:
            print("Episode finished after {} timesteps".format(t+1))
            break
env.close()

print("\n\nBot final weights")
print(bot.QN.get_weights()[-1])

# TODO
# Build an agent class
# Initialise counters
# Build memory system

# First: implement without memory system