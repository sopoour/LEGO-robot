#!/usr/bin/python3
import os
# initialize asebamedulla in background and wait 0.3s to let
# asebamedulla startup
os.system("(asebamedulla ser:name=Thymio-II &) && sleep 0.3")
import matplotlib.pyplot as plt
import numpy as np
import cv2
from picamera import PiCamera
from time import sleep
import dbus
import dbus.mainloop.glib
#from adafruit_rplidar import RPLidar
from math import cos, sin, pi, floor
import threading
import random
import picamera_fps_demo


print("Starting robot")

#-----------------------init script--------------------------
def dbusError(self, e):
    # dbus errors can be handled here.
    # Currently only the error is logged. Maybe interrupt the mainloop here
    print('dbus error: %s' % str(e))


# init the dbus main loop
dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
    
# get stub of the aseba network
bus = dbus.SessionBus()
asebaNetworkObject = bus.get_object('ch.epfl.mobots.Aseba', '/')
    
# prepare interface
asebaNetwork = dbus.Interface(
    asebaNetworkObject,
    dbus_interface='ch.epfl.mobots.AsebaNetwork'
)
    
# load the file which is run on the thymio
asebaNetwork.LoadScripts(
    'thympi.aesl',
    reply_handler=dbusError,
    error_handler=dbusError
)

#signal scanning thread to exit
exit_now = False

#--------------------- init script end -------------------------

#Threshold values
#Wall
#[1] far=1153, close=2081
#[2] far = 1450, close=2019
#[3] far =1388, close=1493
#Ball
#[1] far=1636, catched~1700
#[2] far=1802, close=2059, catched=3082-3517
#[3] far=1635, catched=2233 

wallFar = 1300
wallClose = 1800
#do mainly with middle sensor [2]
ballCatched = 1950
ballAtWall = 3600

def stop(left_wheel, right_wheel):
    left_wheel = 0
    right_wheel = 0
    asebaNetwork.SendEventName(
        'motor.target',
        [left_wheel, right_wheel]
    )

def goBack(left_wheel, right_wheel, velocity):
    left_wheel = -500
    right_wheel = -500
    asebaNetwork.SendEventName(
        'motor.target',
        [left_wheel, right_wheel]
    )

def turnLeft(left_wheel, right_wheel, velocity):
    left_wheel = -velocity
    right_wheel = velocity
    asebaNetwork.SendEventName(
        'motor.target',
        [left_wheel, right_wheel]
    )

def turnRight(left_wheel, right_wheel, velocity):
    left_wheel = velocity
    right_wheel = -velocity/2
    asebaNetwork.SendEventName(
        'motor.target',
        [left_wheel, right_wheel]
    )
def goStraightSlow(left_wheel, right_wheel, velocity):
    left_wheel = velocity
    right_wheel = velocity
    asebaNetwork.SendEventName(
        'motor.target',
        [left_wheel, right_wheel]
    )

def goStraightFast(left_wheel, right_wheel, velocity):
    left_wheel = 500
    right_wheel = 500
    asebaNetwork.SendEventName(
        'motor.target',
        [left_wheel, right_wheel]
    )


def turnAround(left_wheel, right_wheel, velocity):
    left_wheel = velocity
    right_wheel = -velocity/2
    asebaNetwork.SendEventName(
        'motor.target',
        [left_wheel, right_wheel]
    )


def scanning(left_wheel, right_wheel, velocity):
    print("scanning")


def mainLoop():
    #do stuff
    #print(scan_data)  
    print()
    #recordpicamera_fps_demo()
    

#------------------- Main loop end ------------------------

if __name__ == '__main__':
    
    robot = False
    left_wheel = 0
    right_wheel = 0
    velocity = 3000*pi/4
    counter = 0
    dist = 0
    #
    #Where to turn 1 = left 2 = straight, 3 = right
    direction = 0
    ball = False
    backCounter = 0
    x = 0
    y = 0
    
    try:
        while True:
            mainLoop()
            #picamera_fps_demo
            horizontalProximity = asebaNetwork.GetVariable('thymio-II', 'prox.horizontal')
            picamera_fps_demo.direction
            robot = picamera_fps_demo.robot
            #print("direction", direction)
            #TODO: Read variables from OpenCV
            #angle is a counter of 30 degree (250) or 60 degree (500)  
            angle = 0
            #dist = OpenCV reading (0 or 1)
            dist = picamera_fps_demo.dist
            #direction = OpenCV reading (1,2,3)
            direction = picamera_fps_demo.direction
            if(dist == True):
                print("True: short")
                print("direction: ", direction)
                angle = 150
                dist = 300
                ball = True
            else:
                print("False: long")
                print("direction: ", direction)
                angle = 300
                dist = 600
                ball = True

            if (ball == True):
                print("found ball")
                horizontalProximity = asebaNetwork.GetVariable('thymio-II', 'prox.horizontal')
                while (horizontalProximity[1] < ballCatched and horizontalProximity[2] < ballCatched and horizontalProximity[3] < ballCatched and counter < angle + dist):
                    #direction = picamera_fps_demo.direction
                    #print("direction", direction)
                    if(counter < angle):
                        if(direction == 1):
                            turnLeft(left_wheel, right_wheel, velocity)
                            print("turned left")
                        elif(direction == 2):
                            goStraightSlow(left_wheel, right_wheel, velocity)
                            #if robot in the way, avoid
                            print("gone straight")
                        elif(direction == 3):
                            turnRight(left_wheel, right_wheel, velocity)
                            print("turned right")
                        else:
                            print("no ball found")
                    else:
                        goStraightSlow(left_wheel, right_wheel, velocity)
                    counter += 1
                
                if ((horizontalProximity[2] >= ballCatched or horizontalProximity[1] >= ballCatched or horizontalProximity[3] >= ballCatched) and counter >= angle+dist):
                    print("Catched Ball")
                    stop(left_wheel, right_wheel)
                    counter = 0 

            else:
                stop(left_wheel, right_wheel)
                print("no ball")      
                
    except KeyboardInterrupt:
        #print("Stopping robot")
        exit_now = True
        sleep(1)
        #lidar.stop()
        #lidar.disconnect()
        stop(left_wheel, right_wheel)
        os.system("pkill -n -f asebamedulla")
        
        print("asebamodulla killed")
