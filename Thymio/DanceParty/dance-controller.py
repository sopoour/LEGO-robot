import shapely
from shapely.geometry import LinearRing, LineString, Point
from numpy import sin, cos, pi, sqrt
from random import random
import numpy as np

# run using ctrl + alt + N

# Constants
###########
R = 0.02  # radius of wheels in meters
L = 0.094  # distance between wheels in meters

W = 1.15  # width of arena
H = 1.95  # height of arena

robot_timestep = 0.1  # 1/robot_timestep equals update frequency of robot
simulation_timestep = 0.01  # timestep in kinematics sim (probably don't touch..)

# the world is a rectangular arena with width W and height H
world = LinearRing([(W / 2, H / 2), (-W / 2, H / 2), (-W / 2, -H / 2), (W / 2, -H / 2)])

# Variables
###########

x = 0.3  # robot position in meters - x direction
y = 0.0  # robot position in meters - y direction
q = pi/2  # robot heading with respect to x-axis in radians

left_wheel_velocity = 10 / (2 * pi)  # robot left wheel velocity in radians/s
right_wheel_velocity = 10 / (2 * pi)  # robot right wheel velocity in radians/s

# Q-Learning Set-up
####################
gamma = 0.75  # discount factor
alpha = 0.9  # learning rate

# define the rewards
# Columns:sensor_front [short distance, medium distance, long distance], Rows: sensor_left  [short distance, medium distance, long distance]

reward = np.array([
    [-500, -100, 0],
    [-500, 0, 100],
    [-500, 0, 0],
])

# Initializing Q-values & state
Q = np.array(np.zeros([3, 3]))

old_state = -1
state_to_action = -1

def Q_learning_algo(current_state, state_to_action):
    global Q
    # the action here exactly refers to going to the next state
    TD = reward[current_state, state_to_action] + gamma * Q[state_to_action, np.argmax(Q[state_to_action,])] - Q[
        current_state, state_to_action]
    # Update the Q-Value using the Bellman equation
    Q[current_state, state_to_action] += alpha * TD


# Kinematic model
#################
# updates robot position and heading based on velocity of wheels and the elapsed time
# the equations are a forward kinematic model of a two-wheeled robot - don't worry just use it
def simulationstep():
    global x, y, q,state_to_action,old_state

    for step in range(int(robot_timestep / simulation_timestep)):  # step model time/timestep times
        v_x = cos(q) * (R * left_wheel_velocity / 2 + R * right_wheel_velocity / 2)
        v_y = sin(q) * (R * left_wheel_velocity / 2 + R * right_wheel_velocity / 2)
        omega = R * left_wheel_velocity / L - R * right_wheel_velocity / L

        x += v_x * simulation_timestep
        y += v_y * simulation_timestep
        q += omega * simulation_timestep

def sensor_map_to_state(sensorInput):
    if(sensorInput > 30):
        return 2
    elif(13 < sensorInput < 30):
        return 1
    else:
        return 0

def map_sensors(distance_sensor_front, distance_sensor_left):
    if (distance_sensor_front == 0 and distance_sensor_left == 0):
        return 0
    elif (distance_sensor_front == 0 and distance_sensor_left == 1):
        return 0
    elif (distance_sensor_front == 0 and distance_sensor_left == 2):
        return 0
    elif (distance_sensor_front == 1 and distance_sensor_left == 0):
        return 0
    elif (distance_sensor_front == 1 and distance_sensor_left == 1):
        return 0
    elif (distance_sensor_front == 1 and distance_sensor_left == 2):
        return 1
    elif (distance_sensor_front == 2 and distance_sensor_left == 0):
        return 0
    elif (distance_sensor_front == 2 and distance_sensor_left == 1):
        return 1
    elif (distance_sensor_front == 2 and distance_sensor_left == 2):
        return 2


def update_q_table(cnt, current_state):
    # Q_learning_algo Algorithm
    global state_to_action, old_state
    #####################
    # Exploring
    #print("Im going inside the function")
    if (cnt <= 60000 and cnt % 100 == 0) or (cnt < 30000):
        # Pick a random action
        state_to_action = np.random.randint(0, 3)
        #print("Im random")
       # print("Action is now: ", state_to_action)
    # Exploiting 99/100 times from 30000+
    else:
       # print("Im not random")
        state_to_action = np.argmax(Q[current_state])
        #print("Action is now: ", state_to_action)

    Q_learning_algo(current_state, state_to_action)

    old_state = current_state


# Simulation loop
#################
file = open("trajectory.dat", "w")
fileSen = open("sensor.dat", "w")
for cnt in range(100000):
    # simple single-ray sensor
    # print(state_to_action)

    ray_sensor_front = LineString([(x, y), (
    x + cos(q) * 2 * W, y + sin(q) * 2 * H)])  # a line from robot to a point outside arena in direction of q
    ray_sensor_left = LineString([(x, y), (x + cos(q + (pi / 3)) * 2 * W, y + sin(q + (pi / 3)) * 2 * H)])  # a line from robot to a point outside arena in direction of q
    #print(ray_sensor_left)

    sensor_front = world.intersection(ray_sensor_front)
    sensor_left = world.intersection(ray_sensor_left)

    # distance to wall from sensors
    # distance = sqrt((sensor_front.x-x)**2+(sensor_front.y-y)**2)*100
    distance_sensor_front = sensor_map_to_state((sqrt((sensor_front.x - x) ** 2 + (sensor_front.y - y) ** 2) - L / 2) * 100)
    distance_sensor_left = sensor_map_to_state((sqrt((sensor_left.x - x) ** 2 + (sensor_left.y - y) ** 2) - L / 2) * 100)

    #print("front"+str((sqrt((sensor_front.x - x) ** 2 + (sensor_front.y - y) ** 2) - L / 2) * 100))
    #print("L"+str((sqrt((sensor_left.x - x) ** 2 + (sensor_left.y - y) ** 2) - L / 2) * 100))
    # Find current state based on sensor input
    current_state = map_sensors(distance_sensor_front, distance_sensor_left)

    # Update q table if we are in a new state
    if (current_state != old_state or temp_cnt+500<cnt):
        update_q_table(cnt, current_state)
        temp_cnt =cnt
    #if (distance_sensor_front < 50 and distance_sensor_left < 50):
        if state_to_action == 0:
            left_wheel_velocity = -L * pi / 4
            right_wheel_velocity = L * pi / 4
        elif state_to_action == 2:
            left_wheel_velocity = L * pi / 4
            right_wheel_velocity = -L * pi / 4
        else:
            left_wheel_velocity = 10 / (2 * pi)
            right_wheel_velocity = 10 / (2 * pi)

    # step simulation
    simulationstep()

    # check collision with arena walls
    if world.distance(Point(x, y)) < L / 2:
        #print("I'm here"+str(cnt))
        #print(distance_sensor_front)
        #print(distance_sensor_left)
        if x > 0:
            x = x-0.05
        else:
            x = x + 0.05
        if y > 0:
            y = y - 0.05
        else:
            y = y + 0.05
        #print(q)
        q = q + pi/15

    if cnt > 95000:
      if cnt % 50 == 0:
        file.write(str(x) + ", " + str(y) + ", " + str(cos(q) * 0.05) + ", " + str(sin(q) * 0.05) + "\n")
        fileSen.write("Left sensor: " + str(distance_sensor_left) + ", " + "Front sensor: " + str(
        distance_sensor_front) + ", " + "\n")

file.close()
fileSen.close()
print(Q)