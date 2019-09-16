#!/usr/bin/env python3

from ev3dev.ev3 import *
from ev3dev2.sensor.lego import LightSensor
from time import sleep


def loop (lsWh, lsBl, lsM, mBl, mWh) :

    Loop = 10000

    for a in range(0, Loop):
        valueWh = lsWh.value()
        valueBl = lsBl.value()
        valueM = lsM.value()

        mBl.run_forever(speed_sp= 300)
        mWh.run_forever(speed_sp= 300)

        #print (valueWh)
        #sleep(2)
        #on line: 441
        #on edge: 500
        #off line: 540

        if (valueWh < 480 and valueM < 445) or (valueM < 445 and valueBl < 388) :
            intersection(valueWh, valueBl, valueM, mWh, mBl)

        followLine(valueWh, valueBl)


#def planner (valueWh, valueBl, valueM, dir):

def intersection (valueWh, valueBl, valueM, mWh, mBl):
    if valueWh < 480 and valueBl < 388 and valueM < 445 :
        mBl.run_forever(speed_sp= 300)
        mWh.run_forever(speed_sp= 300)

    if valueWh < 480 and valueM < 445 :
        mWh.run_forever(speed_sp=-200)

    if valueM < 445 and valueBl < 388 :
        mBl.run_forever(speed_sp=-200)

def followLine (valueWh, valueBl) :
    #if valueWh < 480 and valueBl < 388 :
     #   mBl.run_forever(speed_sp= 150)

    if valueWh < 478 :
        mBl.run_forever(speed_sp= -300)

    if valueBl < 388 :
        mWh.run_forever(speed_sp= -300)


if __name__ == '__main__':
    # Connect light sensor to input 1 and 4
    lsWh = LightSensor('in4')
    lsBl = LightSensor('in1')
    lsM = LightSensor('in2')
    lsT = TouchSensor('in3')

    mBl = LargeMotor('outB')
    mWh = LargeMotor('outC')

    # Put the Mode_reflect to "Reflect"01
    lsWh.MODE_REFLECT = 'REFLECT'
    lsBl.MODE_REFLECT = 'REFLECT'
    lsM.MODE_REFLECT = 'REFLECT'

    loop(lsBl, lsWh, lsM, mBl, mWh)
