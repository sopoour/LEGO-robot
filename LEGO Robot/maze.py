#!/usr/bin/env python3

from ev3dev.ev3 import *
from ev3dev2.sensor.lego import LightSensor
from time import sleep, time
WHITE_CONS = 600
BLUE_CONS = 550
MIDDLE_CONS = 550

WHITE_CONS_LINE = 460
BLUE_CONS_LINE = 480
MIDDLE_CONS_LINE = 540

SPEED_FORW = 200
SPEED_BACK = -250
i=0
starttime=time()
OurTime=0

#Main loop
def loop (lsWh, lsBl, lsM, mBl, mWh, StartTime, path, robotPos, canPos, canGoal) :

    Loop = 100000

    for a in range(0, Loop):
        valueWh = lsWh.value()
        valueBl = lsBl.value()
        valueM = lsM.value()

        goStraight()
        followLine(lsWh, lsBl, lsM, valueWh, valueBl, valueM, mBl, mWh, StartTime, path, robotPos, canPos, canGoal)

#Basic Behavior of Robot
def followLine (lsWh, lsBl, lsM, valueWh, valueBl, valueM, mBl, mWh, StartTime, path, robotPos, canPos, canGoal) :
    global OurTime
    if (valueWh < WHITE_CONS_LINE and valueBl < BLUE_CONS_LINE and valueM < MIDDLE_CONS_LINE and OurTime < (time() - 3)) or( OurTime+20 >time() and  OurTime < (time() - 3)) :
        Sound.beep()
        nextStep(path, robotPos, canPos, canGoal)

        OurTime = time()

    if valueWh < WHITE_CONS :
        turnLeft()

    if valueBl < BLUE_CONS :
        turnRight()

def turnRight ():
   mWh.run_forever(speed_sp= SPEED_BACK)

def turnLeft():
    mBl.run_forever(speed_sp= SPEED_BACK)

def goStraight():
    mBl.run_forever(speed_sp= SPEED_FORW)
    mWh.run_forever(speed_sp= SPEED_FORW)

#Advanced behavior of Robot related to Sokoban
def turnRightIntersection ():
   mWh.run_to_rel_pos(position_sp=20, speed_sp=SPEED_BACK, stop_action="brake")
   mBl.run_to_rel_pos(position_sp=200, speed_sp=SPEED_BACK, stop_action="brake")
   # wait for both motors to complete their movements
   mWh.wait_while('running')
   mBl.wait_while('running')
   print('RightIntersection')

def turnLeftIntersection():
   mWh.run_to_rel_pos(position_sp=200, speed_sp=SPEED_BACK, stop_action="brake")
   mBl.run_to_rel_pos(position_sp=20, speed_sp=SPEED_BACK, stop_action="brake")
   # wait for both motors to complete their movements
   mWh.wait_while('running')
   mBl.wait_while('running')
   print('LeftIntersection')

def  goStraightIntersection():
    mWh.run_to_rel_pos(position_sp=50, speed_sp=SPEED_BACK, stop_action="brake")
    mBl.run_to_rel_pos(position_sp=50, speed_sp=SPEED_BACK, stop_action="brake")
    # wait for both motors to complete their movements
    mWh.wait_while('running')
    mBl.wait_while('running')
    print('goStraightIntersection')

def  goStraightconer2():
    mWh.run_to_rel_pos(position_sp=70, speed_sp=SPEED_BACK, stop_action="brake")
    mBl.run_to_rel_pos(position_sp=90, speed_sp=SPEED_BACK, stop_action="brake")
    # wait for both motors to complete their movements
    mWh.wait_while('running')
    mBl.wait_while('running')
    print('goStraightIntersection')

def  AroundIntersection():
    mWh.run_to_rel_pos(position_sp=-50, speed_sp=SPEED_BACK, stop_action="brake")
    mBl.run_to_rel_pos(position_sp=-50, speed_sp=SPEED_BACK, stop_action="brake")
    # wait for both motors to complete their movements
    mWh.wait_while('running')
    mBl.wait_while('running')

    mWh.run_to_rel_pos(position_sp=270, speed_sp=SPEED_BACK, stop_action="brake")
    mBl.run_to_rel_pos(position_sp=-270, speed_sp=SPEED_BACK, stop_action="brake")
    # wait for both motors to complete their movements
    mWh.wait_while('running')
    mBl.wait_while('running')
    print(' AroundIntersection')

#Hybrid system taking planner and defined behavior into account

def nextStep(path, robotPos, canPos, canGoal):
    #0 = Up
    #1 = Right
    #2 = Down
    #3 = Left
    global i
    global robotDir

    if robotDir == 0 and i < len(path) - 1:
        #Go straight
        if path[i] - path[i + 1] == 4:
            goStraightIntersection()
        #Turn 180°
        elif path[i] - path[i + 1] == -4:
            robotDir = 2
            AroundIntersection()
        #Go left
        elif path[i] - path[i + 1] == 1:
            robotDir = 3
            turnLeftIntersection()
        #Go right
        elif path[i] - path[i + 1] == -1:
            robotDir = 1
            turnRightIntersection()

    elif robotDir == 1 and i < len(path) - 1:
        #Go left
        if path[i] - path[i + 1] == 4:
            robotDir = 0
            turnLeftIntersection()
        #Go right
        elif path[i] - path[i + 1] == -4:
            robotDir = 2
            turnRightIntersection()
        #Turn 180°
        elif path[i] - path[i + 1] == 1:
            robotDir = 3
            AroundIntersection()
        #Go straight
        elif path[i] - path[i + 1] == -1:
            goStraightIntersection()

    elif robotDir == 2 and i < len(path) - 1:
        #Turn 180°
        if path[i] - path[i + 1] == 4:
            robotDir = 0
            AroundIntersection()
        #Go straight
        elif path[i] - path[i + 1] == -4:
            goStraightIntersection()
        #Go right
        elif path[i] - path[i + 1] == 1:
            robotDir = 3
            turnRightIntersection()
        #Go left
        elif path[i] - path[i + 1] == -1:
            robotDir = 1
            turnLeftIntersection()

    elif robotDir == 3 and i < len(path) - 1:
        #Go right
        if path[i] - path[i + 1] == 4:
            robotDir = 0
            turnRightIntersection()
        #Go left
        elif path[i] - path[i + 1] == -4:
            robotDir = 2
            turnLeftIntersection()
        #Go straight
        elif path[i] - path[i + 1] == 1:
            goStraightIntersection()
        #Turn 180°
        elif path[i] - path[i + 1] == -1:
            robotDir = 1
            AroundIntersection()

    i=i+1




if __name__ == '__main__':
    # Connect light sensor to input 1 and 4
    lsWh = LightSensor('in4')
    lsBl = LightSensor('in1')
    lsM = LightSensor('in2')
    lsT = TouchSensor('in3')

    mBl = LargeMotor('outB')
    mWh = LargeMotor('outC')
    # Put the Mode_reflect to "Reflect"
    lsWh.MODE_REFLECT = 'REFLECT'
    lsBl.MODE_REFLECT = 'REFLECT'
    lsM.MODE_REFLECT = 'REFLECT'

    StartTime = time()
    OurTime = 0
    i=0
    robotPos = 12
    robotDir = 3
    canPos = [8, 4, 6]
    canGoal = [0]

    path = [1,2,3,7,11,15,14,13,12,8,4,0]
    # path = [4,8,12,13,14,15,14,13,12,8,4,5,6,5,1,2,3,7,11,10,6,2,6,10,9,8,9]


    #grid = ['0','1','2','3','4','5','6','7','8','9','10','11','12','13','14','15']

    loop(lsBl, lsWh, lsM, mBl, mWh, StartTime, path, robotPos, canPos, canGoal)
