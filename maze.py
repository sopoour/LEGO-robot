#!/usr/bin/env python3

from ev3dev.ev3 import *
from ev3dev2.sensor.lego import LightSensor
from time import sleep

# Connect light sensor to input 1 and 4
lsWh = LightSensor('in1')
lsBl = LightSensor('in4')
lsM = LightSensor('in2')

mB = LargeMotor('outB')
mC = LargeMotor('outC')

# Put the Mode_reflect to "Reflect"01
lsWh.MODE_REFLECT = 'REFLECT'
lsBl.MODE_REFLECT = 'REFLECT'
lsM.MODE_REFLECT = 'REFLECT'

Loop = 10000

for a in range(0, Loop):
    valueWh = lsWh.value()
    valueBl = lsBl.value()
    valueM = lsM.value()

    mB.run_forever(speed_sp= -400)
    mC.run_forever(speed_sp= -400)

    #print (valueWh)
    #sleep(2)
#on line: 441
#on edge: 500
#off line: 540

    if valueWh < 480 and valueBl < 388 :
        mB.run_forever(speed_sp= -150)

    if valueWh < 478 :
        mB.run_forever(speed_sp= 300)

    if valueBl < 388 :
        mC.run_forever(speed_sp= 300)
