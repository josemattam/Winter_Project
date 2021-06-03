import numpy as np



actions = ['l', 'r', 'u', 'd']
X = 3
Y = 3
Q = np.zeros((X*Y, X*Y, 4)) # first dim is car position, second is trophy,third is actions
class Agent:
    def __init__(self):
        self.alpha = 0.8
        self.discount = 0.8
        self.actions = {'l': 0, 'r': 1, 'u': 2, 'd': 3}
        self.actions_opp = {0: 'l', 1: 'r', 2: 'u', 3: 'd'}
        self.epsilon = 1
        return None
    
    def action(self, state, weird=False):
        positions = self.get_pos(state)
        value_func = Q[positions[0], positions[1]]
        ideal = np.argmax(value_func)
        uni = np.random.uniform()
        if (uni <= self.epsilon) or weird: # weird means choose a random action
            return np.random.choice(actions)
        else:
            return self.actions_opp[ideal]
    
    def train(self, state, action, reward, new_state, success):
        action = self.actions[action]
        state_pos = self.get_pos(state)
        car = state_pos[0]
        trophy = state_pos[1]
        if not success:
            newstate_pos = self.get_pos(new_state)
            carnew = newstate_pos[0]
            trophynew = newstate_pos[1]
            Q[car, trophy, action] += self.alpha * (reward + self.discount*max(Q[carnew, trophynew]) - Q[car, trophy, action])
        elif success:
            Q[car, trophy, action] = reward
            self.epsilon -= 0.007
        # update Q value at state_pos[0], state_pos[1]
        print("Q updated")
        

    def get_pos(self, state):
        # given state, get position as an int of car and trophy
        car = np.where(state==1)
        trophy = np.where(state==2)
        car = car[0][0]*Y + car[1][0]
        trophy = trophy[0][0]*Y + trophy[1][0]
        return (car, trophy)

class Game:
    def __init__(self):
        print("Game created")
        X = 3
        Y = 3
        self.state = np.zeros((X, Y))
        startx = np.random.randint(X)
        starty = np.random.randint(Y)

        self.state[startx, starty] = 1

        trophyx = np.random.randint(X)
        trophyy = np.random.randint(Y)

        while (startx==trophyx) and (starty==trophyy):
            trophyx = np.random.randint(X)
            trophyy = np.random.randint(Y)

        self.state[trophyx, trophyy] = 2

        self.actions = ['l', 'r', 'u', 'd']
        self.success = False
        return None
    
    def play(self, action):
        pos = np.where(self.state==1)
        self.state[pos] = 0
        pos = [pos[0][0], pos[1][0]]
        if action=='l':
            pos[1] -= 1
            print("left")
        elif action=='r':
            pos[1] += 1
            print("right")
        elif action=='u':
            pos[0] -= 1
            print("up")
        elif action=='d':
            pos[0] += 1
            print("down")
        else:
            print("Invalid action")
        unadjusted_pos = [i for i in pos]
        pos[0] = max(0, pos[0])
        pos[0] = min(X-1, pos[0])
        pos[1] = max(0, pos[1])
        pos[1] = min(X-1, pos[1])
        reward = -10*np.any(np.array(pos) != np.array(unadjusted_pos))
        pos = (np.array([pos[0]]), np.array([pos[1]]))
        if self.state[pos] == 2:
            print("Success!")
            self.success = True
            reward = 10
            return reward
        else:
            self.state[pos] = 1
            return reward
        
        
    def get_state(self):
        return self.state

a = Agent()
episodes = 100
for n in range(episodes):
    g = Game()
    print("\n\nEPISODE", n+1)
    while not g.success:
        state = 1.0*g.get_state()
        action = a.action(state)
        reward = g.play(action)
        # print(g.success)
        # print("reward: ", reward)
        # print(state)
        # print(g.get_state())
        a.train(state, action, reward, g.get_state(), g.success)

print("\n\nTRAINING COMPLETE ({} EPISODES)\n\n".format(episodes))
a.epsilon = 0 # no more exploration
def test(weird=False):
    print("test")
    g = Game()
    while not g.success:
        state = 1.0*g.get_state()
        action = a.action(state, weird)
        reward = g.play(action)
        print(state)
        print(g.success)
        print("reward: ", reward)
        print(g.get_state())
