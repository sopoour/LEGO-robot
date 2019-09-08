#!/usr/bin/env python3

from ev3dev.ev3 import *
from ev3dev2.sensor.lego import LightSensor
from time import sleep

# Connect light sensor to input 1 and 4
lsWh = LightSensor('in1')
lsBl = LightSensor('in4')

mB = LargeMotor('outB')
mC = LargeMotor('outC')

# Put the Mode_reflect to "Reflect"
lsWh.MODE_REFLECT = 'REFLECT'
lsBl.MODE_REFLECT = 'REFLECT'

Loop = 1000

file1 = open("test.txt", "w")
for a in range(0, Loop):
    valueWh = lsWh.value()
    valueBl = lsBl.value()

    mB.run_forever(speed_sp = 400)
    mC.run_forever(speed_sp = 400)
    if valueWh < 500 :
        mB.stop()
        sleep(5)
    if valueBl < 500 :
        mC.stop()
        sleep(5)






