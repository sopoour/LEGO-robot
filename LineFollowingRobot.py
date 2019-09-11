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

Loop = 10000

for a in range(0, Loop):
    valueWh = lsWh.value()
    valueBl = lsBl.value()

    mB.run_forever(speed_sp= -300)
    mC.run_forever(speed_sp= -300)


    if valueWh < 480 :
        mB.run_forever(speed_sp= 300)

    if valueBl < 390 :
        mC.run_forever(speed_sp= 300)

    mB.run_forever(speed_sp= -400)
    mC.run_forever(speed_sp= -400)

    #print (valueWh)
    #sleep(2)
    if valueBl < 482 and valueWh < 392 :
        mB.run_forever(speed_sp= -150)

    if valueWh < 482 :
        mB.run_forever(speed_sp= 300)

    if valueBl < 392 :
        mC.run_forever(speed_sp= 300)








