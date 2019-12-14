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

# Setup the RPLidar
#PORT_NAME = '/dev/ttyUSB0'
#lidar = RPLidar(None, PORT_NAME)
#This is where we store the lidar readings
#scan_data = [0]*360
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
ballCatched = 2500
ballAtWall = 3600

def recordpicamera_fps_demo():
    camera = PiCamera()
    camera.vflip = True
    camera.hflip = True

    try:
        camera.resolution = (640, 480)
        camera.start_recording('rec.h264')
        camera.wait_recording(5)
        camera.stop_recording()
        os.system("MP4Box -add rec.h264 rec.mp4")
        #Delete h264 file
        os.system("rm rec.h264")
    finally:
        camera.close()

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


#NOTE: if you get adafruit_rplidar.RPLidarException: Incorrect descriptor starting bytes
# try disconnecting the usb cable and reconnect again. That should fix the issue
def lidarScan():
    print("Starting background lidar scanning")
    for scan in lidar.iter_scans():
        if(exit_now):
            return
        for (_, angle, distance) in scan:
            scan_data[min([359, floor(angle)])] = distance

#scanner_thread = threading.Thread(target=lidarScan)
#scanner_thread.daemon = True
#scanner_thread.start()

#def testLidar():
 #   print(scan_data)

#------------------ Main loop here -------------------------

def mainLoop():
    #do stuff
    #print(scan_data)  
    print()
    #recordpicamera_fps_demo()
    

#------------------- Main loop end ------------------------

if __name__ == '__main__':
    #Initialize picamera_fps_demo readings
    #color = ''
    robot = False
    #ball = False
   
    #testLidar()

    #Initialize Thymio
    left_wheel = 0
    right_wheel = 0
    velocity = 3000*pi/4
    counter = 0
    #Color 1 = Red, 2 = Green, 3 = Blue
    homeColor = 1

    #State 0 = Turn around, 1 = Check Ball, 2 = Move to ball, 3 = Catch Ball, 4 = home
    state = 0
    homePosition = 3
    #Distance 0 = short, 1 = long
    dist = 0
    #
    #Where to turn 1 = left 2 = straight, 3 = right
    direction = 2
    ball = False
    start = True
    backCounter = 0
    x = 0
    y = 0
    
    try:
        while True:
            mainLoop()
            #picamera_fps_demo
            horizontalProximity = asebaNetwork.GetVariable('thymio-II', 'prox.horizontal')

            #Finding position
            if(state == 0):
                print("Find position")
                state = 1
            #Turn 180 degrees and go straight to center if it is the start of the game  
            elif(state == 1):
                while(counter < 1500):
                    turnAround(left_wheel, right_wheel, velocity)
                    counter += 1
                if(counter >= 1500):
                    stop(left_wheel, right_wheel)
                    print("stop & state 2!")
                    counter = 0
                    state = 2
                if(start == True):
                    print("go to center, push balls and then go home")   
                    #TODO: Figure for how long the counter should run
                    while(counter < 15500):
                        if(counter < 14000):
                            counter_avoid = 0
                            goStraightFast(left_wheel, right_wheel, velocity)
                            start = False
                        else:
                            turnAround(left_wheel, right_wheel, velocity)
                            print("go home")
                            #goHome()
                            #if robot in the way, avoid
                            robot = picamera_fps_demo.robot
                            if (robot == True):
                                while(counter_avoid < 2000):
                                    if (counter_avoid < 600):
                                        turnLeft(left_wheel, right_wheel, velocity)
                                    else:
                                        goStraightFast(left_wheel, right_wheel, velocity)
                                    counter_avoid += 1
                        counter += 1
                    if (counter >= 15500):
                        counter = 0    
                        print("start: stop & state=2")
                        stop(left_wheel, right_wheel)
                        state = 2

            #Detect ball and drive towards it
            if(state == 2):
                picamera_fps_demo.direction
                #recordpicamera_fps_demo()
                robot = picamera_fps_demo.robot
                #direction = picamera_fps_demo.direction 
                #print("direction", direction)
                #TODO: Read variables from OpenCV
                #angle is a counter of 30 degree (250) or 60 degree (500)  
                angle = 0
                #dist = OpenCV reading (0 or 1)
                dist = picamera_fps_demo.dist
                #direction = OpenCV reading (1,2,3)
                direction = picamera_fps_demo.direction
                if(dist == True):
                    print("short")
                    print("direction ", direction)
                    angle = 200
                    dist = 300
                    ball = True
                else:
                    print("long")
                    print("direction ", direction)
                    angle = 400
                    dist = 600
                    ball = True

                if (ball == True):
                    horizontalProximity = asebaNetwork.GetVariable('thymio-II', 'prox.horizontal')
                    while (horizontalProximity[1] < ballCatched and horizontalProximity[2] < ballCatched and horizontalProximity[3] < ballCatched and counter < angle + dist):
                        #direction = picamera_fps_demo.direction
                        #print("direction", direction)
                        if(counter < angle):
                            if(direction == 3):
                                turnLeft(left_wheel, right_wheel, velocity)
                                #print("turned left")
                            elif(direction == 2):
                                goStraightSlow(left_wheel, right_wheel, velocity)
                                #if robot in the way, avoid
                                #recordpicamera_fps_demo()
                                if (robot == True):
                                    print("avoid robo")
                                #print("gone straight")
                            elif(direction == 1):
                                turnRight(left_wheel, right_wheel, velocity)
                                #print("turned right")
                        else:
                            goStraightSlow(left_wheel, right_wheel, velocity)
                            #if robot in the way, avoid
                            robot = picamera_fps_demo.robot
                            if (robot == True):
                                while(counter_avoid < 2000):
                                    if (counter_avoid < 200):
                                        turnLeft(left_wheel, right_wheel, velocity)
                                    else:
                                        goStraightFast(left_wheel, right_wheel, velocity)
                                    counter_avoid += 1
                                if (counter_avoid >= 2000):
                                    counter_avoid = 0
                        counter += 1
                    
                    if (horizontalProximity[2] >= ballCatched and counter >= angle+dist):
                        print("Catched Ball")
                        stop(left_wheel, right_wheel)
                        state = 3
                        counter = 0 

                else:
                    while(backCounter < 2000 or horizontalProximity[1] < ballCatched and horizontalProximity[2] < ballCatched and horizontalProximity[3] < ballCatched):
                        goBack(left_wheel, right_wheel, velocity)
                        turnLeft(left_wheel, right_wheel, velocity)
                        backCounter += 1
                    backCounter = 0
                            
            #Move ball to the enemy field go forward until we hit a wall
            elif(state == 3):
                print("Move forward")
                while (counter < 5000):
                    counter += 1
                    if((horizontalProximity[1] < ballAtWall and horizontalProximity[2] < ballAtWall) or (horizontalProximity[3] < ballAtWall and horizontalProximity[2] < ballAtWall)):
                        print("Bring ball to wall")
                        goStraightFast(left_wheel, right_wheel, velocity)
                        #if robot in the way, avoid
                        #recordpicamera_fps_demo()
                        robot = picamera_fps_demo.robot
                        if (robot == True):
                            while(counter_avoid < 2000):
                                if (counter_avoid < 200):
                                    turnLeft(left_wheel, right_wheel, velocity)
                                else:
                                    goStraightFast(left_wheel, right_wheel, velocity)
                                counter_avoid += 1
                            if (counter_avoid >= 2000):
                                counter_avoid = 0
                        
                        
                #utrn around either if counter is over or it recognizes the wall
                if (counter >= 5000 or ((horizontalProximity[1] >= ballAtWall and horizontalProximity[2] >= ballAtWall) or (horizontalProximity[3] >= ballAtWall and horizontalProximity[2] >= ballAtWall))):
                    counter = 0
                    while(counter < 3500):
                        if (counter < 2000):
                            goBack(left_wheel, right_wheel, velocity)
                            print("Backing")
                        else:
                            print("After Backing, turn around!")
                            turnAround(left_wheel, right_wheel, velocity)
                        counter += 1  
                    if(counter >= 3500):
                        stop(left_wheel, right_wheel)
                        counter = 0
                        state = 4
                        print("stop and go home!")
                else:    
                    while(backCounter < 2000):
                        goBack(left_wheel, right_wheel, velocity)
                        backCounter += 1
                    backCounter = 0
            elif(state == 4):
                color = picamera_fps_demo.color
                randomAction = random.randint(0,1)
                while(color != homeColor or counter < 4000):
                    color = picamera_fps_demo.color
                    if(counter < 1000):
                        if(randomAction == 0):
                            turnLeft(left_wheel, right_wheel, velocity)
                        elif(randomAction == 1):
                            turnRight(left_wheel, right_wheel, velocity)
                    else:
                        randomAction = random.randint(0,1)
                    counter += 1
                counter = 0
                while(counter < 3000):
                    goStraightFast(left_wheel, right_wheel, velocity)
                    counter += 1
                
                if(counter >= 3000):
                    counter = 0
                    state = 1
                print("back in state 4")

#Todo test state 4
#Todo avoid robots
                    
            
                
    except KeyboardInterrupt:
        #print("Stopping robot")
        exit_now = True
        sleep(1)
        #lidar.stop()
        #lidar.disconnect()
        stop(left_wheel, right_wheel)
        os.system("pkill -n -f asebamedulla")
        
        print("asebamodulla killed")
