# import the necessary packages
from __future__ import print_function
from imutils.video.pivideostream import PiVideoStream
from imutils.video import FPS
from picamera.array import PiRGBArray
from picamera import PiCamera
import argparse
import imutils
import time
import cv2
import numpy as np
import os


#To make them global:
#Color 1 = Red, 2 = Green, 3 = Blue
color = 0
robot = False
#ball = False
#Color values are hue values

# 3 = Left, 2 = Straight, 1 = Right
direction = 0
# True = Short, False = Long
dist = False
    
# Crop picture left, middle, right, short, long
xLeftMin = 0
xLeftMax = 320

xMiddleMin = 320
xMiddleMax = 340

xRightMin = 340
xRightMax = 640

yShort = 0
yMedium = 240
yLong = 480
 
# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-n", "--num-frames", type=int, default=100,
	help="# of frames to loop over for FPS test")
ap.add_argument("-d", "--display", type=int, default=-1,
	help="Whether or not frames should be displayed")
args = vars(ap.parse_args())
 
# initialize the camera and stream
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
camera.vflip = True
camera.hflip = True

rawCapture = PiRGBArray(camera, size=(640, 480))
stream = camera.capture_continuous(rawCapture, format="bgr",
	use_video_port=True)
camera.capture('/home/pi/image.jpg')

# allow the camera to warmup and start the FPS counter
print("[INFO] sampling frames from `picamera` module...")
time.sleep(2.0)
fps = FPS().start()
 
# loop over some frames
for (i, f) in enumerate(stream):
    # grab the frame from the stream and resize it to have a maximum
    # width of 400 pixels
    frame = f.array
    #frame = imutils.resize(frame, width=480)
    longLeft = frame[yShort:yMedium,xLeftMin:xLeftMax]
    longMiddle = frame[yShort:yMedium,xMiddleMin:xMiddleMax]
    longRight = frame[yShort:yMedium,xRightMin:xRightMax]
    shortLeft = frame[yMedium:yLong,xLeftMin:xLeftMax]
    shortMiddle = frame[yMedium:yLong,xMiddleMin:xMiddleMax]
    shortRight = frame[yMedium:yLong,xRightMin:xRightMax]
    
    hsvLongLeft =cv2.cvtColor(longLeft, cv2.COLOR_BGR2HSV)
    hsvLongMiddle =cv2.cvtColor(longMiddle, cv2.COLOR_BGR2HSV)
    hsvLongRight =cv2.cvtColor(longRight, cv2.COLOR_BGR2HSV)
    hsvShortLeft =cv2.cvtColor(shortLeft, cv2.COLOR_BGR2HSV)
    hsvShortMiddle =cv2.cvtColor(shortMiddle, cv2.COLOR_BGR2HSV)
    hsvShortRight =cv2.cvtColor(shortRight, cv2.COLOR_BGR2HSV)
    #Red
    red_lower_hsv = np.array([90, 150, 130])
    red_upper_hsv = np.array([255, 255, 255])
    redLongLeft = cv2.inRange(hsvLongLeft, red_lower_hsv, red_upper_hsv) 
    redLongMiddle = cv2.inRange(hsvLongMiddle, red_lower_hsv, red_upper_hsv) 
    redLongRight = cv2.inRange(hsvLongRight, red_lower_hsv, red_upper_hsv) 
    #redShortLeft = cv2.inRange(hsvShortLeft, red_lower_hsv, red_upper_hsv) 
    #redShortMiddle = cv2.inRange(hsvShortMiddle, red_lower_hsv, red_upper_hsv)
    #redShortRight = cv2.inRange(hsvShortRight, red_lower_hsv, red_upper_hsv)  

    #Blue
    blue_lower_hsv = np.array([90, 125, 104])
    blue_upper_hsv = np.array([160, 255, 255])
    blueLongLeft = cv2.inRange(hsvLongLeft, blue_lower_hsv, blue_upper_hsv) 
    blueLongMiddle = cv2.inRange(hsvLongMiddle, blue_lower_hsv, blue_upper_hsv) 
    blueLongRight = cv2.inRange(hsvLongRight, blue_lower_hsv, blue_upper_hsv) 
    #blueShortLeft = cv2.inRange(hsvShortLeft, blue_lower_hsv, blue_upper_hsv) 
    #blueShortMiddle = cv2.inRange(hsvShortMiddle, blue_lower_hsv, blue_upper_hsv) 
    #blueShortRight = cv2.inRange(hsvShortRight, blue_lower_hsv, blue_upper_hsv) 
    

    #Green
    green_lower_hsv = np.array([30, 51, 91])
    green_upper_hsv = np.array([90, 255, 255])
    greenLongLeft = cv2.inRange(hsvLongLeft, green_lower_hsv, green_upper_hsv) 
    greenLongMiddle = cv2.inRange(hsvLongMiddle, green_lower_hsv, green_upper_hsv) 
    greenLongRight = cv2.inRange(hsvLongRight, green_lower_hsv, green_upper_hsv) 

    #Robot
    robot_lower_hsv = np.array([0, 0, 0])
    robot_upper_hsv = np.array([40, 50, 50])
    robotLongLeft = cv2.inRange(hsvLongLeft, robot_lower_hsv, robot_upper_hsv)
    robotLongMiddle = cv2.inRange(hsvLongMiddle, robot_lower_hsv, robot_upper_hsv)
    robotLongRight = cv2.inRange(hsvLongRight, robot_lower_hsv, robot_upper_hsv)

    #Yellow ball
    yellow_lower_hsv = np.array([29, 86, 6])
    yellow_upper_hsv = np.array([64, 255, 255])
    yellowShortLeft = cv2.inRange(hsvLongLeft, yellow_lower_hsv, yellow_upper_hsv)
    yellowShortMiddle = cv2.inRange(hsvLongMiddle, yellow_lower_hsv, yellow_upper_hsv)
    yellowShortRight = cv2.inRange(hsvLongRight, yellow_lower_hsv, yellow_upper_hsv)
    yellowLongLeft = cv2.inRange(hsvShortLeft, yellow_lower_hsv, yellow_upper_hsv)
    yellowLongMiddle = cv2.inRange(hsvShortMiddle, yellow_lower_hsv, yellow_upper_hsv)
    yellowLongRight = cv2.inRange(hsvShortRight, yellow_lower_hsv, yellow_upper_hsv)

    #Sum colors
    redsumLongLeft = np.sum(redLongLeft)
    redsumLongMiddle = np.sum(redLongMiddle)
    redsumLongRight = np.sum(redLongRight)

    greensumLongLeft = np.sum(greenLongLeft)
    greensumLongMiddle = np.sum(greenLongMiddle)
    greensumLongRight = np.sum(greenLongRight)

    bluesumLongLeft = np.sum(blueLongLeft)
    bluesumLongMiddle = np.sum(blueLongMiddle)
    bluesumLongRight = np.sum(blueLongRight)

    yellowsumShortLeft = np.sum(yellowLongLeft)
    yellowsumShortMiddle = np.sum(yellowLongMiddle)
    yellowsumShortRight = np.sum(yellowLongRight)
    yellowsumLongLeft = np.sum(yellowShortLeft)
    yellowsumLongMiddle = np.sum(yellowShortMiddle)
    yellowsumLongRight = np.sum(yellowShortRight)

    robotsumLongLeft = np.sum(robotLongLeft)
    robotsumLongMiddle = np.sum(robotLongMiddle)
    robotsumLongRight = np.sum(robotLongRight)

    min = 500
    minrobot = 2000

    #cv2.imshow('frame', frame)
    #cv2.imshow("LeftShort", shortLeft)
    #cv2.imshow("LeftLong", longLeft)
    #cv2.imshow("MiddleShort", shortMiddle)
    #cv2.imshow("MiddleLong", longMiddle)
    #cv2.imshow("RightShort", shortRight)
    #cv2.imshow("RightLong", longRight)

    print("yellowsumShortLeft", yellowsumShortLeft)
    print("yellowsumShortMiddle", yellowsumShortMiddle)
    print("yellowsumShortRight", yellowsumShortRight)
    print("yellowsumLongLeft", yellowsumLongLeft)
    print("yellowsumLongMiddle", yellowsumLongMiddle)
    print("yellowsumLongRight", yellowsumLongRight)

    #Check if we see a robot
    if(robotsumLongLeft > minrobot or robotsumLongMiddle > minrobot or robotsumLongRight > minrobot):
        robot = True
        print("robot")
    
    if yellowsumShortLeft > min and yellowsumShortLeft > yellowsumShortMiddle and yellowsumShortLeft > yellowsumShortRight and yellowsumShortLeft > yellowsumLongLeft and yellowsumShortLeft > yellowsumLongMiddle and yellowsumShortLeft > yellowsumLongRight:
        print("yellowsumShortLeft")
        direction = 1
        dist = True

    elif yellowsumShortMiddle > min and yellowsumShortMiddle > yellowsumShortLeft and yellowsumShortMiddle > yellowsumShortRight and yellowsumShortMiddle > yellowsumLongLeft and yellowsumShortMiddle > yellowsumLongMiddle and yellowsumShortMiddle > yellowsumLongRight:
        print("yellowsumShortMiddle")
        direction = 2
        dist = True
    
    elif yellowsumShortRight > min and yellowsumShortRight > yellowsumShortLeft and yellowsumShortRight > yellowsumShortMiddle and yellowsumShortRight > yellowsumLongLeft and yellowsumShortRight > yellowsumLongMiddle and yellowsumShortRight > yellowsumLongRight:
        print("yellowsumShortRight")
        direction = 3
        dist = True

    elif yellowsumLongLeft > min and yellowsumLongLeft > yellowsumShortLeft and yellowsumLongLeft > yellowsumShortMiddle and yellowsumLongLeft > yellowsumShortRight and yellowsumLongLeft > yellowsumLongMiddle and yellowsumLongLeft > yellowsumLongRight:
      print("yellowsumLongLeft")
      direction = 1
      #  dist = False
    
    elif yellowsumLongMiddle > min and yellowsumLongMiddle > yellowsumShortLeft and yellowsumLongMiddle > yellowsumShortMiddle and yellowsumLongMiddle > yellowsumShortRight and yellowsumLongMiddle > yellowsumLongLeft and yellowsumLongMiddle > yellowsumLongRight:
        print("yellowsumLongMiddle")
        direction = 2
        dist = False
    
    elif yellowsumLongRight > min or yellowsumLongRight > yellowsumShortLeft and yellowsumLongRight > yellowsumShortMiddle and yellowsumLongRight > yellowsumShortRight and yellowsumLongRight > yellowsumLongLeft and yellowsumLongRight > yellowsumLongMiddle:
        print("yellowsumLongRight")
        direction = 3
        dist = False

    if redsumLongLeft > redsumLongMiddle and redsumLongLeft > redsumLongRight and redsumLongLeft > greensumLongLeft and redsumLongLeft > greensumLongMiddle and redsumLongLeft > greensumLongRight and redsumLongLeft > bluesumLongLeft and redsumLongLeft > bluesumLongMiddle and redsumLongLeft > bluesumLongRight:
        color = 1
    elif redsumLongMiddle > redsumLongLeft and redsumLongMiddle > redsumLongRight and redsumLongMiddle > greensumLongLeft and redsumLongMiddle > greensumLongMiddle and redsumLongMiddle > greensumLongRight and redsumLongMiddle > bluesumLongLeft and redsumLongMiddle > bluesumLongMiddle and redsumLongMiddle > bluesumLongRight:
        color = 1
    elif redsumLongRight > redsumLongLeft and redsumLongRight > redsumLongMiddle and redsumLongLeft > greensumLongLeft and redsumLongLeft > greensumLongMiddle and redsumLongLeft > greensumLongRight and redsumLongLeft > bluesumLongLeft and redsumLongLeft > bluesumLongMiddle and redsumLongLeft > bluesumLongRight:
        color = 1
    elif greensumLongLeft > redsumLongLeft and greensumLongLeft > redsumLongMiddle and greensumLongLeft > redsumLongRight and greensumLongLeft > greensumLongMiddle and greensumLongLeft > greensumLongRight and greensumLongLeft > bluesumLongLeft and greensumLongLeft > bluesumLongMiddle and greensumLongLeft > bluesumLongRight:
        color = 2
    elif greensumLongMiddle > redsumLongLeft and greensumLongMiddle > redsumLongMiddle and greensumLongMiddle > redsumLongRight and greensumLongMiddle > greensumLongLeft and greensumLongMiddle > greensumLongRight and greensumLongMiddle > bluesumLongLeft and greensumLongMiddle > bluesumLongMiddle and greensumLongMiddle > bluesumLongRight:
        color = 2
    elif greensumLongRight > redsumLongLeft and greensumLongRight > redsumLongMiddle and greensumLongRight > redsumLongRight and greensumLongRight > greensumLongMiddle and greensumLongRight > greensumLongLeft and greensumLongRight > bluesumLongLeft and greensumLongRight > bluesumLongMiddle and greensumLongRight > bluesumLongRight:
        color = 2
    elif bluesumLongLeft > redsumLongLeft and bluesumLongLeft > redsumLongMiddle and bluesumLongLeft > redsumLongRight and bluesumLongLeft > greensumLongMiddle and bluesumLongLeft > greensumLongLeft and bluesumLongLeft > greensumLongRight and bluesumLongLeft > bluesumLongMiddle and bluesumLongLeft > bluesumLongRight:
        color = 3
    elif bluesumLongMiddle > redsumLongLeft and bluesumLongMiddle > redsumLongMiddle and bluesumLongMiddle > redsumLongRight and bluesumLongMiddle > greensumLongMiddle and bluesumLongMiddle > greensumLongLeft and bluesumLongMiddle > greensumLongRight and bluesumLongMiddle > bluesumLongLeft and bluesumLongMiddle > bluesumLongRight:
        color = 3
    elif bluesumLongRight > redsumLongLeft and bluesumLongRight > redsumLongMiddle and bluesumLongRight > redsumLongRight and bluesumLongRight > greensumLongMiddle and bluesumLongRight > greensumLongLeft and bluesumLongRight > greensumLongRight and bluesumLongRight > bluesumLongLeft and bluesumLongRight > bluesumLongMiddle:
        color = 3
    print("direction", direction)
    print(dist)	
 
    # check to see if the frame should be displayed to our screen
    if args["display"] > 0:
        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1) & 0xFF

    # clear the stream in preparation for the next frame and update
    # the FPS counter
    rawCapture.truncate(0)
    fps.update()

    # check to see if the desired number of frames have been reached
    if i == args["num_frames"] or direction != 0 or color != 0:
        break
 
# stop the timer and display FPS information
fps.stop()
print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

#camera.start_recording('rec.h264')
#camera.wait_recording(5)
#camera.stop_recording()
#os.system("MP4Box -add rec.h264 rec.mp4")
# do a bit of cleanup
cv2.destroyAllWindows()
stream.close()
rawCapture.close()
camera.close()

# created a *threaded *video stream, allow the camera sensor to warmup,
# and start the FPS counter
print("[INFO] sampling THREADED frames from `picamera` module...")
vs = PiVideoStream().start()
time.sleep(2.0)
fps = FPS().start()
#cv2.imshow()
 
# loop over some frames...this time using the threaded stream
while fps._numFrames < args["num_frames"]:
    # grab the frame from the threaded video stream and resize it
    # to have a maximum width of 400 pixels
    frame = vs.read()
    frame = imutils.resize(frame, width=400)

    # check to see if the frame should be displayed to our screen
    if args["display"] > 0:
        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1) & 0xFF

    # update the FPS counter
    fps.update()
 
# stop the timer and display FPS information
fps.stop()
print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))
 
# do a bit of cleanup
cv2.destroyAllWindows()
vs.stop()