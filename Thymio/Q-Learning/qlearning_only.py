import numpy as np

##We need 1. environment, 2. action, 3. state, 4. reward
gamma = 0.75 # discount factor
alpha = 0.9 # learning rate

#define the actions
#0 = Left
#1 = Straight
#2 = Right

actions = [0, 1, 2]

#define the rewards
#Columns:
#actions [left, straight, right]
#Rows: 
#states [short distance, medium distance, long distance]

reward = np.array ([
[-500,-500,0], 
[100,0,0], 
[0,10,0],
])

def policy ():
    #copy the rewards matrix to a new matrix
    #reward_env_new = np.copy(reward_env)

    #----Q-learning algorithm-----
    
    #Initializing Q-values
    Q = np.array(np.zeros([3,3]))

    #Q-learning process
    for i in range(1000):
        playable_actions = []
        #Pick-up state randomly
        current_state = np.random.randint(0,3)
        #Iterate through the new rewards matrix and get the actions > 0
       
        for j in range(3):
            playable_actions.append(j)
        #Pick an action randomly from the list of playable actions leading us to the next state
        next_state = np.random.choice(playable_actions)
       
        #Compute the temporal difference
        #the action here exactly refers to going to the next state
        TD = reward[current_state, next_state] + gamma * Q[next_state, np.argmax(Q[next_state,])] - Q[current_state, next_state]
        #Update the Q-Value using the Bellman equation
        Q[current_state,next_state] += alpha * TD

    #We do not know about the next location yet, so initialize with the value of starting location
    print(Q)

policy()