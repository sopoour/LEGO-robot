import numpy as np
import random
from controller import Robot, Motor

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
sens2 = robot.getDistanceSensor("prox.horizontal.2")
sens4 = robot.getDistanceSensor("prox.horizontal.4")
#enable distance sensor measurements in sampling period of TIME_STEP
sens2.enable(TIME_STEP)
sens4.enable(TIME_STEP)

class ThymioRobot:
    def __init__(self, id, gender, startPos, sensor_front, sensor_right):
        self.id = id
        self.gender = gender
        self.startPos = startPos
        self.sensor_front = sensor_front
        self.sensor_right = sensor_right

    # Choose random gender
    ##############
    # 0 = male = blue
    # 1 = female = red
    def generateGender(self):
        random.randint(0, 1)

    def generateStartPosition(self):
        random.random()

p1 = ThymioRobot()
p1.myfunc()

#Wall following algorithm

while robot.step(TIME_STEP) != -1:
    #get the values read by the sensor
    sens2_dist = sens2.getValue()
    sens4_dist = sens4.getValue()
    
    
    if sens4_dist > dist:
       #Turn left
       leftMotor.setVelocity(-dist*3.14159265359/4)
       rightMotor.setVelocity(dist*3.14159265359/4)
    
    else: 
       leftMotor.setVelocity(0.1 * MAX_SPEED)
       rightMotor.setVelocity(0.1 * MAX_SPEED)
       



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