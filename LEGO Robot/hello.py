#!/usr/bin/env python3


import os
import sys
import time
import math
from ev3dev.ev3 import *
from time import sleep

diameter = 0.0816
axelDia = 0.095
x=-0.32
y=1.4
theta=-90
axelDiaM = axelDia*math.pi/360
C = diameter*math.pi/360
hy = math.sqrt(math.pow(x,2) +math.pow(y,2))
StartV= math.degrees(math.cosh(x/hy))

# Attach large motors to ports B and C
mB = LargeMotor('outB')
mC = LargeMotor('outC')


mB.run_to_rel_pos(position_sp=axelDiaM*400/C, speed_sp=450, stop_action="brake")
mC.run_to_rel_pos(position_sp=-axelDiaM*400/C, speed_sp=450, stop_action="brake")

# wait for both motors to complete their movements

mB.wait_while('running')
mC.wait_while('running')
sleep(2)

# Make the robot turn
mB.run_to_rel_pos(position_sp=axelDiaM*StartV/C, speed_sp=450, stop_action="brake")
mC.run_to_rel_pos(position_sp=-axelDiaM*StartV/C, speed_sp=450, stop_action="brake")

# wait for both motors to complete their movements

mB.wait_while('running')
mC.wait_while('running')
sleep(2)
# Make the robot advance such that the wheels rotate 720 deg
# (50% speed, apply brake when movement terminated).
# Assuming speed_sp=900 gives full speed then
# speed_sp=450 gives 50% speed
mB.run_to_rel_pos(position_sp=(hy/C), speed_sp=450, stop_action="brake")
mC.run_to_rel_pos(position_sp=(hy/C), speed_sp=450, stop_action="brake")

# wait for both motors to complete their movements

mB.wait_while('running')
mC.wait_while('running')

sleep(1) # Wait one second

# Make the robot turn
mB.run_to_rel_pos(position_sp=(-axelDiaM*theta/C)+(-axelDiaM*StartV/C), speed_sp=450, stop_action="brake")
mC.run_to_rel_pos(position_sp=(axelDiaM*theta/C)+(axelDiaM*StartV/C), speed_sp=450, stop_action="brake")

# wait for both motors to complete their movements

mB.wait_while('running')
mC.wait_while('running')
sleep(2)
