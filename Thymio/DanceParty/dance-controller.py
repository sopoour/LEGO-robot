import shapely
from shapely.geometry import LinearRing, LineString, Point
from numpy import sin, cos, pi, sqrt
from random import random
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
        omega = R*right_wheel_velocity/L - left_wheel_velocity/L    
    
        x += v_x * simulation_timestep
        y += v_y * simulation_timestep
        q += omega * simulation_timestep

# Simulation loop
#################
file = open("trajectory.dat", "w")
fileSen = open("sensor.dat", "w")
for cnt in range(5000):
    # simple single-ray sensor
    # a line from robot to a point outside arena in direction of q
    ray_sensor_front = LineString([(x, y), (x + cos(q) * 2 * W, y + sin(q) * 2 * H)])  
    ray_sensor_right = LineString([(x, y), (x + cos(q + (pi / 3)) * 2 * W, y + sin(q + (pi / 3)) * 2 * H)])  
    #print(ray_sensor_left)

    sensor_front = world.intersection(ray_sensor_front)
    sensor_right = world.intersection(ray_sensor_right)

    # distance to wall from sensors
    # distance = sqrt((sensor_front.x-x)**2+(sensor_front.y-y)**2)*100
    distance_sensor_front = sqrt(((sensor_front.x - x) ** 2 + (sensor_front.y - y) ** 2))
    distance_sensor_right = sqrt(((sensor_right.x - x) ** 2 + (sensor_right.y - y) ** 2))
      
    #simple controller - change direction of wheels every 10 seconds (100*robot_timestep) unless close to wall then turn on spot
    if cnt%100==0:            
        if (distance_sensor_front < 0.15 and distance_sensor_right < 0.15):
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
        fileSen.write("Right sensor: " + str(distance_sensor_right) + ", " + "Front sensor: " + str(
        distance_sensor_front) + ", " + "\n")

file.close()
fileSen.close()

#asebamedulla "ser:name=Thymio-II"
    
