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

starttime=time()



def loop (lsWh, lsBl, lsM, mBl, mWh, StartTime, OurTime, path, robotPos, robotDir, canPos, canGoal) :

    Loop = 10000

    for a in range(0, Loop):
        valueWh = lsWh.value()
        valueBl = lsBl.value()
        valueM = lsM.value()

        goStraight()
        followLine(lsWh, lsBl, lsM, valueWh, valueBl, valueM, mBl, mWh, OurTime, StartTime, path, robotPos, robotDir, canPos, canGoal)


def followLine (lsWh, lsBl, lsM, valueWh, valueBl, valueM, mBl, mWh, OurTime, StartTime, path, robotPos, robotDir, canPos, canGoal) :
    if valueWh < WHITE_CONS_LINE and valueBl < BLUE_CONS_LINE and valueM < MIDDLE_CONS_LINE and OurTime < (StartTime - 2):
        Sound.beep()
        nextStep(path, robotPos, robotDir, canPos, canGoal)
        OurTime = StartTime

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

def turnRightIntersection ():
   mWh.run_to_rel_pos(position_sp=20, speed_sp=SPEED_BACK, stop_action="brake")
   mBl.run_to_rel_pos(position_sp=180, speed_sp=SPEED_BACK, stop_action="brake")
   # wait for both motors to complete their movements
   mWh.wait_while('running')
   mBl.wait_while('running')

def turnLeftIntersection ():
   mWh.run_to_rel_pos(position_sp=180, speed_sp=SPEED_BACK, stop_action="brake")
   mBl.run_to_rel_pos(position_sp=20, speed_sp=SPEED_BACK, stop_action="brake")
   # wait for both motors to complete their movements
   mWh.wait_while('running')
   mBl.wait_while('running')

def  goStraightIntersection():
    mWh.run_to_rel_pos(position_sp=150, speed_sp=SPEED_BACK, stop_action="brake")
    mBl.run_to_rel_pos(position_sp=150, speed_sp=SPEED_BACK, stop_action="brake")
    # wait for both motors to complete their movements
    mWh.wait_while('running')
    mBl.wait_while('running')

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

<<<<<<< HEAD
def nextStep(path, robotPos, robotDir, canPos, canGoal):
    #0 = Up
    #1 = Right
    #2 = Down
    #3 = Left

    if robotDir == 0:
        for i in path - 1:
            #Go straight
            if path[i] - path[i + 1] == 4:
                goStraightIntersection()
            #Turn 180°
            if path[i] - path[i + 1] == -4:
                robotDir = 2
                AroundIntersection()
            #Go left
            if path[i] - path[i + 1] == 1:
                robotDir = 3
                turnLeftIntersection()
            #Go right
            if path[i] - path[i + 1] == -1:
                robotDir = 1
                turnRightIntersection()

    if robotDir == 1:
        for i in path:
            #Go left
            if path[i] - path[i + 1] == 4:
                robotDir = 0
                turnLeftIntersection()
            #Go right
            if path[i] - path[i + 1] == -4:
                robotDir = 2
                turnRightIntersection()
            #Turn 180°
            if path[i] - path[i + 1] == 1:
                robotDir = 3
                AroundIntersection()
            #Go straight
            if path[i] - path[i + 1] == -1:
                goStraightIntersection()

    if robotDir == 2:
        for i in path:
            #Turn 180°
            if path[i] - path[i + 1] == 4:
                robotDir = 0
                AroundIntersection()
            #Go straight
            if path[i] - path[i + 1] == -4:
                goStraightIntersection()
            #Go right
            if path[i] - path[i + 1] == 1:
                robotDir = 3
                turnRightIntersection()
            #Go left
            if path[i] - path[i + 1] == -1:
                robotDir = 1
                turnLeftIntersection()

    if robotDir == 3:
        for i in path:
            #Go right
            if path[i] - path[i + 1] == 4:
                robotDir = 0
                turnRightIntersection()
            #Go left
            if path[i] - path[i + 1] == -4:
                robotDir = 2
                turnLeftIntersection()
            #Go straight
            if path[i] - path[i + 1] == 1:
                goStraightIntersection()
            #Turn 180°
            if path[i] - path[i + 1] == -1:
                robotDir = 1
                AroundIntersection()


=======
>>>>>>> ae4df2553cc84fdfd1fe70a422b698d9c8c745d7


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

    robotPos = 12
    robotDir = 0
    canPos = [8, 4, 6]
    canGoal = [0]

    path = [12, 8, 4]

    #grid = ['0','1','2','3','4','5','6','7','8','9','10','11','12','13','14','15']

    loop(lsBl, lsWh, lsM, mBl, mWh, StartTime, OurTime, path, robotPos, robotDir, canPos, canGoal)
