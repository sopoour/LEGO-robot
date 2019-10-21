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
#states [corner left, corner right, left-wall, right-wall, nothing, wall]

reward_env = np.array ([
[-100,-100,10], 
[10,-100,-100], 
[-100,10,-10],
[-10,10,-100],
[0,50, 0],
[10,-100,10]])


#q_matrix = [
#[0,0,0], 
#[0,0,0], 
#[0,0,0], 
#[0,0,0],
#[0,0,0],
#[0,0,0],
#[0,0,0],
#[0,0,0],
#[0,0,0]]

def policy (starting_position):
    #copy the rewards matrix to a new matrix
    #reward_env_new = np.copy(reward_env)

    #----Q-learning algorithm-----
    
    #Initializing Q-values
    Q = np.array(np.zeros([6,3]))

    current_state = starting_position
    #Q-learning process
    for i in range(2):
        playable_actions = []
        #Pick-up state randomly
        current_state = np.random.randint(0,6)
        #Iterate through the new rewards matrix and get the actions > 0
        print("Current_state: ", current_state)
        for j in range(3):
            playable_actions.append(j)
        #Pick an action randomly from the list of playable actions leading us to the next state
        next_state = np.random.choice(playable_actions)
        print("Next_state: ", next_state)
        #Compute the temporal difference
        #the action here exactly refers to going to the next state
        TD = reward_env[current_state, next_state] + gamma * Q[next_state, np.argmax(Q[next_state,])] - Q[current_state, next_state]
        #Update the Q-Value using the Bellman equation
        Q[current_state,next_state] += alpha * TD

    #We do not know about the next location yet, so initialize with the value of starting location
    print(Q)

policy(0)