#!/usr/bin/env python3

from ev3dev.ev3 import *
from ev3dev2.sensor.lego import LightSensor
from time import sleep

BLUE_CONS = 480
WHITE_CONS = 470
MIDDLE_CONS = 500

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

        if (valueWh < WHITE_CONS and valueM < MIDDLE_CONS) or (valueM < MIDDLE_CONS and valueBl < BLUE_CONS) :
            intersection(valueWh, valueBl, valueM, mWh, mBl)

        else :
            followLine(valueWh, valueBl)


#def planner (valueWh, valueBl, valueM, dir):

def intersection (valueWh, valueBl, valueM, mWh, mBl):
    #if valueWh < WHITE_CONS and valueBl < BLUE_CONS and valueM < MIDDLE_CONS :
    #    mBl.run_forever(speed_sp= 300)
    #    mWh.run_forever(speed_sp= 300)

    if valueWh < WHITE_CONS and valueM < MIDDLE_CONS :
        mWh.run_forever(speed_sp=-200)

    elif valueM < MIDDLE_CONS and valueBl < BLUE_CONS :
        mBl.run_forever(speed_sp=-200)

def followLine (valueWh, valueBl) :
    if valueWh < WHITE_CONS and valueBl < BLUE_CONS :
        mBl.run_forever(speed_sp= 150)
        mWh.run_forever(speed_sp= 150)

    elif valueWh < WHITE_CONS :
        mBl.run_forever(speed_sp= -300)

    elif valueBl < BLUE_CONS :
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
