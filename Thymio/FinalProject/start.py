#!/usr/bin/python3
import matplotlib
matplotlib.use('Agg')
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
from adafruit_rplidar import RPLidar
from math import cos, sin, pi, floor
import threading


print("Starting robot")

#-----------------------init script--------------------------
camera = PiCamera()

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
PORT_NAME = '/dev/ttyUSB0'
lidar = RPLidar(None, PORT_NAME)
#This is where we store the lidar readings
scan_data = [0]*360
#--------------------- init script end -------------------------

def testCamera():
    print("Camera test")
    camera.start_preview()
    sleep(5)
    #we capture to openCV compatible format
    #you might want to increase resolution
    camera.resolution = (320, 240)
    camera.framerate = 24
    sleep(2)
    image = np.empty((240, 320, 3), dtype=np.uint8)
    camera.capture(image, 'bgr')
    cv2.imwrite('out.png', image) 
    camera.stop_preview()
    print("saved image to out.png")

def cameraReadings():
    #color
    if(color == 1):
        print("green")
        #green
    elif(color == 2):
        print("blue")
        #blue
    elif(color == 3):
        print("red")
        #red
    
    if(ball):
        
    #ball

def stop(left_wheel, right_wheel):
    left_wheel = 0
    right_wheel = 0

def turnLeft(left_wheel, right_wheel, velocity):
    left_wheel = -velocity
    right_wheel = velocity

def turnRight(left_wheel, right_wheel, velocity):
    left_wheel = velocity
    right_wheel = -velocity

def goStraightSlow(left_wheel, right_wheel, velocity):
    left_wheel = velocity
    right_wheel = velocity

def goStraightFast(left_wheel, right_wheel, velocity):
    left_wheel = velocity * 2
    right_wheel = Velocity * 2

def turnAround(left_wheel, right_wheel, velocity):
    left_wheel = velocity*pi
    right_wheel = 0

def scanning(left_wheel, right_wheel, velocity):
    print("scanning")

def thymioController():
    left_wheel = 0
    right_wheel = 0
    velocity = 3000*pi/4
    turnAround(left_wheel, right_wheel, velocity)
    stop(left_wheel, right_wheel)
    asebaNetwork.SendEventName(
        'motor.target',
        [left_wheel, right_wheel]
    )
    print("motor should be running now")
    sleep(5)
    asebaNetwork.SendEventName(
        'motor.target',
        [0, 0]
    )


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

def testLidar():
    print(scan_data)

#------------------ Main loop here -------------------------

def mainLoop():
    #do stuff
    #print(scan_data)  
    print("hi")

#------------------- Main loop end ------------------------

if __name__ == '__main__':
    #testCamera()
    thymioController()
    #testLidar()
    try:
        while True:
            mainLoop()
            
    except KeyboardInterrupt:
        print("Stopping robot")
        exit_now = True
        sleep(1)
        #lidar.stop()
        #lidar.disconnect()
        os.system("pkill -n asebamedulla")

        print("asebamodulla killed")