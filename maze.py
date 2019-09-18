#!/usr/bin/env python3

from ev3dev.ev3 import *
from ev3dev2.sensor.lego import LightSensor
from time import sleep


# Values for WHITE
# OFF: 655-658
# EDGE: 670-676
# ON: 431

#Values for BLUE:
# OFF: 640-642
# EDGE: 630-636
# ON: 471

#Values for MIDDLE:
# OFF: 733-746
# EDGE: 714-722
# ON: 482-519

BLUE_CONS = 480
WHITE_CONS = 500
MIDDLE_CONS = 500

SPEED_FORW = 300
SPEED_BACK = -250

def loop (lsWh, lsBl, lsM, mBl, mWh) :

    Loop = 10000

    Wcu = 0
    Bcu = 0
    for a in range(0, Loop):
        valueWh = lsWh.value()
        valueBl = lsBl.value()
        valueM = lsM.value()

        goStraight()
        #if (valueWh < WHITE_CONS and valueM < MIDDLE_CONS) or (valueM < MIDDLE_CONS and valueBl < BLUE_CONS) :
            #intersection(valueWh, valueBl, valueM, mWh, mBl)

        #else :
        followLine(Bcu, Wcu, lsWh, lsBl, valueWh, valueBl)


#def planner (valueWh, valueBl, valueM, dir):

def intersection (mWh, mBl):
    #if valueWh < WHITE_CONS and valueBl < BLUE_CONS and valueM < MIDDLE_CONS :
    #    mBl.run_forever(speed_sp= 300)
    #    mWh.run_forever(speed_sp= 300)

    #if valueWh < WHITE_CONS and valueM < MIDDLE_CONS :
     #   mWh.run_forever(speed_sp=SPEED_BACK)

    #elif valueM < MIDDLE_CONS and valueBl < BLUE_CONS :
     #   mBl.run_forever(speed_sp=SPEED_BACK)
    #turnLeft()
    sleep(2)
    turnLeft()

def followLine (Bcu, Wcu, lsWh, lsBl, valueWh, valueBl) :
    #if valueWh < WHITE_CONS and valueBl < BLUE_CONS :
     #   goStraight()

    if valueWh < WHITE_CONS :
        if valueBl < BLUE_CONS :
            intersection(mWh, mBl)
        else :
            goStraight()
            newVal1 = lsBl.value()
            if newVal1 < BLUE_CONS :
                intersection(mWh, mBl)

    elif valueBl < BLUE_CONS :
        if valueWh < WHITE_CONS :
            intersection(mWh, mBl)
        else :
            goStraight()
            newVal1 = lsWh.value()
            if newVal1 < WHITE_CONS :
                intersection(mWh, mBl)



def turnRight ():
    mWh.run_forever(speed_sp= SPEED_BACK)

def turnLeft():
    mBl.run_forever(speed_sp= SPEED_BACK)

def goStraight():
    mBl.run_forever(speed_sp= SPEED_FORW)
    mWh.run_forever(speed_sp= SPEED_FORW)


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
