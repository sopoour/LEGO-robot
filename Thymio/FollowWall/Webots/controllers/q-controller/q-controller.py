import numpy as np
from controller import Robot, Motor

#-------General-----------
TIME_STEP = 64

MAX_SPEED = 6.28

#distance to the wall
dist = 12

# create the Robot instance.
robot = Robot()

#See Thymio specific Webots names: https://cyberbotics.com/doc/guide/thymio2#thymio2-wbt
#See "robot" specific functions: https://cyberbotics.com/doc/reference/robot?tab=python#getlightsensor
#Motors
leftMotor = robot.getMotor('motor.left')
rightMotor = robot.getMotor('motor.right')
leftMotor.setPosition(float('inf'))
rightMotor.setPosition(float('inf'))
leftMotor.setVelocity(0)
rightMotor.setVelocity(0)

#see functions of DistanceSensor: https://cyberbotics.com/doc/reference/distancesensor#wb_distance_sensor_enable
#sensors
sens0 = robot.getDistanceSensor("prox.horizontal.0")
sens1 = robot.getDistanceSensor("prox.horizontal.1")
sens2 = robot.getDistanceSensor("prox.horizontal.2")
sens3 = robot.getDistanceSensor("prox.horizontal.3")
sens4 = robot.getDistanceSensor("prox.horizontal.4")
#enable distance sensor measurements in sampling period of TIME_STEP
sens0.enable(TIME_STEP)
sens1.enable(TIME_STEP)
sens2.enable(TIME_STEP)
sens3.enable(TIME_STEP)
sens4.enable(TIME_STEP)



#-------Q-Setup---------------
gamma = 0.75 # discount factor
alpha = 0.9 # learning rate

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

def currentState ():
    #get the values read by the sensor
    sens0_dist = sens0.getValue()
    sens1_dist = sens1.getValue()
    sens2_dist = sens2.getValue()
    sens3_dist = sens3.getValue()
    sens4_dist = sens4.getValue()
    
    if sens0_dist > dist and sens1_dist > dist and sens2_dist > dist:
        return 0
    elif sens2_dist > dist and sens3_dist > dist and sens4_dist > dist:
        return 1
    elif sens0_dist > dist and sens1_dist:
        return 2
    elif sens3_dist > dist and sens4_dist:
        return 3
    elif sens0_dist > dist and sens1_dist > dist and sens2_dist > dist and sens3_dist > dist and sens4_dist > dist:
        return 5
    else:
        return 4
    

#---------Q-Learning Algorithm------------

Q = np.array(np.zeros([6,3]))

#Q-learning process
for i in range(1000):
    playable_actions = []
    #Pick-up state randomly
    current_state = currentState()
    #Iterate through the new rewards matrix and get the actions > 0
    for j in range(3):
        playable_actions.append(j)
    #Pick an action randomly from the list of playable actions leading us to the next state
    next_state = np.random.choice(playable_actions)
    #Compute the temporal difference
    #the action here exactly refers to going to the next state
    TD = reward_env[current_state, next_state] + gamma * Q[next_state, np.argmax(Q[next_state,])] - Q[current_state, next_state]
    #Update the Q-Value using the Bellman equation
    Q[current_state,next_state] += alpha * TD
    
    if next_state == 0:
       #Turn left
       leftMotor.setVelocity(-dist*3.14159265359/4)
       rightMotor.setVelocity(dist*3.14159265359/4)
       
    elif next_state == 1:
       leftMotor.setVelocity(0.1 * MAX_SPEED)
       rightMotor.setVelocity(0.1 * MAX_SPEED)
       
    elif next_state == 2:
        #Turn Right
       leftMotor.setVelocity(dist*3.14159265359/4)
       rightMotor.setVelocity(-dist*3.14159265359/4)
    else:
       leftMotor.setVelocity(0.1 * MAX_SPEED)
       rightMotor.setVelocity(0.1 * MAX_SPEED)
    
    print("Current state: ", current_state)
    print("Next state: ", next_state)  
       