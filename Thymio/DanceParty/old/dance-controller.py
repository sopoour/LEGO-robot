import shapely
from shapely.geometry import LinearRing, LineString, Point
from numpy import sin, cos, pi, sqrt
from random import random
import time
import random
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

# Communication
##############
#Todo: change
def startCommunication(distance_sensor_front, distance_sensor_right):
    returnToRest(distance_sensor_front, distance_sensor_right)

#Todo: change
def acknowledgeCommunication(distance_sensor_front, distance_sensor_right):
    returnToRest(distance_sensor_front, distance_sensor_right)

#Todo: change
def shutDownCommunication(distance_sensor_front, distance_sensor_right):
    returnToRest(distance_sensor_front, distance_sensor_right)

#Todo: change
#return true if asked to dance
def checkIfAskedToDance(distance_sensor_front, distance_sensor_right):
    returnToRest(distance_sensor_front, distance_sensor_right)

# Behaviours 
############

# The robots randomly decide on a gender and change their color to reﬂect their gender 
# (blue, red) 1. The robot is shy at the moment and stays still along the wall. 
# It timidly awaits another robot to ask it to dance.
def benchWarmer(distance_sensor_front, distance_sensor_right):
    #Another robot can ask it to dnace
    startCommunication(distance_sensor_front, distance_sensor_right)
    isSingle = True
    start = time.time()
    end = time.time()
    gender = chooseGender()
    while(isSingle and (start-end <= 30)):
        end = time.time()
        if(checkIfAskedToDance()):
            isSingle = False
        print(gender)
    isSingle = True
    returnToRest(distance_sensor_front, distance_sensor_right)
    #If it gets an acknowledgement it transistions to dance
    #dance()

# Once in a while the robot has built up enough courage and starts navigating along the wall 
# counter clock-wise and around any robots in its way. If it locates a robot of the opposite 
# gender it asks it to dance, which is always accepted because robots are nice. 
# If it has not found a partner for a while it settles down again.
#Todo
#Stay further from wall?
#Detect other robots
#If opposite gender ask to dance
#If a partner with the oppossite gender is detected, 
#it communicates acknowledge ﬁve times after which it transistions to dance.

def findDancePartner(cnt, distance_sensor_front):
    global left_wheel_velocity, right_wheel_velocity
    start = time.time()
    end = time.time()
    while(end-start <= 30):
        if cnt%100==0:   
            if (distance_sensor_front < 0.5):
                left_wheel_velocity = L*pi/4
                right_wheel_velocity = -L*pi/4
            else:                
                left_wheel_velocity = 10/(2*pi)
                right_wheel_velocity = 10/(2*pi)
        end = time.time()
    #If it has not found a robot for a while (30sec) it settles down again
    returnToRest(distance_sensor_front, distance_sensor_right)


#Todo 
#Turn purple
#Navigate to the center of the arena 
#Do a wild dance with robot
def danceMoves():
    global left_wheel_velocity, right_wheel_velocity, x, y
    start = time.time()
    end = time.time()
    #Navigate to the center of the arena
    #Todo: change
    x = 0.0
    y = 0.0
    #Dance for 15 seconds
    while(end-start <= 15):
        #Dance
        left_wheel_velocity = -L*pi/4
        right_wheel_velocity = L*pi/4
        end = time.time()
    returnToRest(distance_sensor_front, distance_sensor_right)

# Todo
# The robots return to the perimeter of the arena and ﬁnd a free spot away from other robots 
# and faces the arena
def returnToRest(distance_sensor_front, distance_sensor_right):
    global left_wheel_velocity, right_wheel_velocity
    #Go to the perimeter of the arena
    while(distance_sensor_front > 0.15):
        left_wheel_velocity = 10/(2*pi)
        right_wheel_velocity = 10/(2*pi)
    
    #Face arena
    faceArena(distance_sensor_right)
    left_wheel_velocity = 0
    right_wheel_velocity = 0

def faceArena(distance_sensor_right):
    global left_wheel_velocity, right_wheel_velocity
    #Turn 180°
    #Todo: check if correct
    while(distance_sensor_right > 0.15):
        left_wheel_velocity = L*pi/4
        right_wheel_velocity = -L*pi/4

# Reading Sensor values
#######################
def distanceSensorFront():
    global left_wheel_velocity, x, y
    ray_sensor_front = LineString([(x, y), (x + cos(q) * 2 * W, y + sin(q) * 2 * H)])  
    sensor_front = world.intersection(ray_sensor_front)
    distance_sensor_front = sqrt(((sensor_front.x - x) ** 2 + (sensor_front.y - y) ** 2))
    return distance_sensor_front

def distanceSensorRight():
    global right_wheel_velocity, x, y
    ray_sensor_right = LineString([(x, y), (x + cos(q + (pi / 3)) * 2 * W, y + sin(q + (pi / 3)) * 2 * H)])  
    sensor_right = world.intersection(ray_sensor_right)
    distance_sensor_right = sqrt(((sensor_right.x - x) ** 2 + (sensor_right.y - y) ** 2))
    return distance_sensor_right

# Simulation loop
#################
file = open("./DanceParty/trajectory.dat", "w")
fileSen = open("./DanceParty/sensor.dat", "w")
for cnt in range(5000):
    #Get distance to wall for both front and right sensor
    distance_sensor_front = distanceSensorFront()
    distance_sensor_right = distanceSensorRight()
    
    #benchWarmer(distance_sensor_front, distance_sensor_right)
    #showColor()
    #findDancePartner(cnt, distance_sensor_front)
    #danceMoves()   
    #step simulation
    simulationstep()

    #check collision with arena walls 
    if (world.distance(Point(x,y))<L/2):
        break
        
    if cnt%50==0:
        file.write( str(x) + ", " + str(y) + ", " + str(cos(q)*0.05) + ", " + str(sin(q)*0.05) + "\n")
        fileSen.write("Right sensor: " + str(distance_sensor_right) + ", " + "Front sensor: " + str(
        distance_sensor_front) + ", " + "\n")

file.close()
fileSen.close()

#asebamedulla "ser:name=Thymio-II"
    
