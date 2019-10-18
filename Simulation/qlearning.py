import numpy as np

##We need 1. environment, 2. action, 3. state, 4. reward
gamma = 0.75 # discount factor
alpha = 0.9 # learning rate

#define the state in an environment of 9x9
location_to_state = {
    "L1": 0,
    "L2": 1,
    "L3": 2,
    "L4": 3,
    "L5": 4,
    "L6": 5,
    "L7": 6,
    "L8": 7,
    "L9": 8
}

#set of actions is nothing but the set of all possible states of the robot
#define the actions
#0 = Front
#1 = Right
#2 = Back
#3 = Left
actions = [0,1,2,3,4,5,6,7,8]

#
#define the rewards
rewards = np.array([[0,1,0,0,0,0,0,0,0],
[1,0,1,0,0,0,0,0,0],
[0,1,0,0,0,1,0,0,0],
[0,0,0,0,0,0,1,0,0],
[0,1,0,0,0,0,0,1,0],
[0,0,1,0,0,0,0,0,0],
[0,0,0,1,0,0,0,1,0],
[0,0,0,0,1,0,1,0,1],
[0,0,0,0,0,0,0,1,0]])

#Maps indices to locations
state_to_location = dict((state, location) for location, state in location_to_state.items())

def policy (start_location, end_location):
    #copy the rewards matrix to a new matrix
    rewards_new = np.copy(rewards)
    #Get the ending state corresponding to the ending location as given
    ending_state = location_to_state[end_location]
    #with the above informataion automatically set the priority of the given ending state to the highest one
    rewards_new[ending_state, ending_state] = 999

    #----Q-learning algorithm-----
    
    #Initializing Q-values
    Q = np.array(np.zeros([9,9]))

    #Q-learning process
    for i in range(1000):
        #Pick-up state randomly
        current_state = np.random.randint(0,9) #Python excludes the upper bound
        #For traversing through the neighbor locations in the maze
        playable_actions = []
        #Iterate through the new rewards matrix and get the actions > 0
        for j in range(9):
            if rewards_new[current_state,j] > 0:
                playable_actions.append(j)
        #Pick an action randomly from the list of playable actions leading us to the next state
        next_state = np.random.choice(playable_actions)
        #Compute the temporal difference
        #the action here exactly refers to going to the next state
        TD = rewards_new[current_state, next_state] + gamma * Q[next_state, np.argmax(Q[next_state,])] - Q[current_state, next_state]
        #Update the Q-Value using the Bellman equation
        Q[current_state,next_state] += alpha * TD
    
    #Initialize the optimal route with the starting location
    route = [start_location]
    #We do not know about the next location yet, so initialize with the value of starting location
    next_location = start_location

    #Update the environment
    #We don't know about the exact number of iterations needed to reach to the final location hence while loop will be good a choice for the iteration
    while(next_location != end_location):
        #Fetch the starting state
        starting_state = location_to_state[start_location]
        #Fetch the highest Q-value pertaining to starting state
        next_state = np.argmax(Q[starting_state,])
        #We got the index of the next state. But we need the corresponding letter
        next_location = state_to_location[next_state]
        route.append(next_location)
        #Update the starting location for the next iteration
        start_location = next_location

    return route

print(policy("L9", "L1"))