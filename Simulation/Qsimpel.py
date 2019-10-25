import shapely
from shapely.geometry import LinearRing, LineString, Point
from numpy import sin, cos, pi, sqrt
from random import random
import numpy as np
#run using ctrl + alt + N

# Constants
###########
R = 0.02  # radius of wheels in meters
L = 0.094  # distance between wheels in meters

W = 1.15  # width of arena
H = 1.95  # height of arena

robot_timestep = 0.1        # 1/robot_timestep equals update frequency of robot
simulation_timestep = 0.01  # timestep in kinematics sim (probably don't touch..)

# the world is a rectangular arena with width W and height H
world = LinearRing([(W/2,H/2),(-W/2,H/2),(-W/2,-H/2),(W/2,-H/2)])

# Variables 
###########

x = 0.0   # robot position in meters - x direction
y = 0.0   # robot position in meters - y direction
q = 0.0   # robot heading with respect to x-axis in radians 

left_wheel_velocity =  10/(2*pi)  # robot left wheel velocity in radians/s
right_wheel_velocity =  10/(2*pi)  # robot right wheel velocity in radians/s


# Q-Learning Set-up
####################
gamma = 0.75 # discount factor
alpha = 0.9 # learning rate

#define the rewards
#Columns:actions [left, straight, right], Rows: states [short distance, medium distance, long distance]
reward = np.array ([
[-50,-50, 0], 
[0,0,50], 
[0,0,0],
])

#Initializing Q-values
Q = np.array(np.zeros([3,3]))

#Map distance to state (short, medium, long)
def dist_map_state(x):
    if x > 15:
       return 2
    elif 13 < x <= 15:
       return 1
    else:
        return 0

# Kinematic model
#################
# updates robot position and heading based on velocity of wheels and the elapsed time
# the equations are a forward kinematic model of a two-wheeled robot - don't worry just use it
def simulationstep():
    global x, y, q

    for step in range(int(robot_timestep/simulation_timestep)):     #step model time/timestep times
        v_x = cos(q)*(R*left_wheel_velocity/2 + R*right_wheel_velocity/2) 
        v_y = sin(q)*(R*left_wheel_velocity/2 + R*right_wheel_velocity/2)
        omega = R*left_wheel_velocity/L - R*right_wheel_velocity/L    
    
        x += v_x * simulation_timestep
        y += v_y * simulation_timestep
        q += omega * simulation_timestep

def merge_dist (distS0, distS2):
    if distS0 == 0 or distS2 == 0:
        return 0
    elif distS0 == 1 or distS2 == 1:
        return 1
    else:
        return 2

# Simulation loop
#################
file = open("trajectory.dat", "w")
fileSen = open("sensor.dat", "w")
for cnt in range(100000):
    #Sensor and Distance Set-up
    ###########################
    #simple single-ray for each sensor 
    ray0 = LineString([(x, y), (x+cos(q+(pi/3))*2*W,y+sin(q+(pi/3))*2*H) ])  # a line from robot to a point outside arena in direction of q
    ray2 = LineString([(x, y), (x+cos(q)*2*W,y+sin(q)*2*H) ])  # a line from robot to a point outside arena in direction of q
    #ray4 = LineString([(x, y), (x+cos(q-(pi/3))*2*W,y+sin(q-(pi/3))*2*H) ])  # a line from robot to a point outside arena in direction of q

    #Left sensor
    s0 = world.intersection(ray0)
    #Front sensor
    s2 = world.intersection(ray2)
    #Right sensor
    #s4 = world.intersection(ray4)
    
    #distance = sqrt((s.x-x)**2+(s.y-y)**2)                 
    #distance to wall
    distS0 = dist_map_state((sqrt((s0.x-x)**2+(s0.y-y)**2)-L)*100) 
    distS2 =dist_map_state((sqrt((s2.x-x)**2+(s2.y-y)**2)-L) *100)
    #distS4 = dist_map_state((sqrt((s4.x-x)**2+(s4.y-y)**2)-L)*100)

    #Q_learning Algorithm
    #####################

    #Pick-up state randomly
    current_state = merge_dist(distS0, distS2)
    
    #Pick an action randomly from the list of playable actions leading us to the next state
    next_state = np.random.randint(0,3)
    
    #Compute the temporal difference
    #the action here exactly refers to going to the next state
    TD = reward[current_state, next_state] + gamma * Q[next_state, np.argmax(Q[next_state,])] - Q[current_state, next_state]
    #Update the Q-Value using the Bellman equation
    Q[current_state,next_state] += alpha * TD    

    #Controller = Action Mapping
    ###########
   
    #simple controller - change direction of wheels every 10 seconds (100*robot_timestep) unless close to wall then turn on spot           
    if next_state == 0:
        left_wheel_velocity = -L*pi/4
        right_wheel_velocity = L*pi/4
    elif next_state == 1:
       left_wheel_velocity = 10/(2*pi)
       right_wheel_velocity = 10/(2*pi)
    else:                
        left_wheel_velocity = L*pi/4
        right_wheel_velocity = -L*pi/4
    
    #step simulation
    simulationstep()

    #check collision with arena walls 
    if (world.distance(Point(x,y))<L/2):
        break
        
    if cnt%50==0:
        file.write( str(x) + ", " + str(y) + ", " + str(cos(q)*0.05) + ", " + str(sin(q)*0.05) + "\n")
        fileSen.write( str(distS0) + ", " + str(distS2) + "\n")

print(Q)
file.close()
fileSen.close()

    
