import shapely
from shapely.geometry import LinearRing, LineString, Point
from numpy import sin, cos, pi, sqrt
from random import random
import numpy as np
#run using ctrl + alt + N

Q_tabel =  np.zeros((3,5), dtype=int)

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

def clamp(x):
   if x > 15:
       return 15
   n=0     
   while(x>0):
       x=x-1
       n=n+1
   return n

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

# Simulation loop
#################
file = open("trajectory.dat", "w")
fileSen = open("sensor.dat", "w")
for cnt in range(5000):
    #simple single-ray sensor
    
    ray = LineString([(x, y), (x+cos(q)*2*W,y+sin(q)*2*H) ])  # a line from robot to a point outside arena in direction of q
    ray0 = LineString([(x, y), (x+cos(q+(pi/3))*2*W,y+sin(q+(pi/3))*2*H) ])  # a line from robot to a point outside arena in direction of q
    ray4 = LineString([(x, y), (x+cos(q-(pi/3))*2*W,y+sin(q-(pi/3))*2*H) ])  # a line from robot to a point outside arena in direction of q
     

    s = world.intersection(ray)
    s0 = world.intersection(ray0)
    s4 = world.intersection(ray4)
    
    distance = sqrt((s.x-x)**2+(s.y-y)**2)                 # distance to wall
    distanceS2 =clamp((sqrt((s.x-x)**2+(s.y-y)**2)-L) *100)
    
    distancesS0 = clamp((sqrt((s0.x-x)**2+(s0.y-y)**2)-L)*100) 
    distancesS4 = clamp((sqrt((s4.x-x)**2+(s4.y-y)**2)-L)*100)    

    #simple controller - change direction of wheels every 10 seconds (100*robot_timestep) unless close to wall then turn on spot
    if cnt%100==0:            
        if (distance < 0.5):
            left_wheel_velocity = -L*pi/4
            right_wheel_velocity = L*pi/4
        else:                
            left_wheel_velocity = 10/(2*pi)
            right_wheel_velocity = 10/(2*pi)
        
    #step simulation
    simulationstep()

    #check collision with arena walls 
    if (world.distance(Point(x,y))<L/2):
        break
        
    if cnt%50==0:
        file.write( str(x) + ", " + str(y) + ", " + str(cos(q)*0.05) + ", " + str(sin(q)*0.05) + "\n")
        fileSen.write( str(distancesS0) + ", " + str(distanceS2) + ", " + str(distancesS4)   + "\n")

file.close()
fileSen.close()

    
