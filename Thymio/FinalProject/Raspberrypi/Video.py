import cv2
import numpy as np
import os

#cap = cv2.VideoCapture(0)
#For testing the colors from a video:
#cap = cv2.VideoCapture('Green/green.mp4')
#cap = cv2.VideoCapture('Blue/blue.mp4')
#cap = cv2.VideoCapture('Red/red.mp4')
#cap = cv2.VideoCapture('Balls/yellow-balls.mp4')

cap = cv2.VideoCapture('rec.mp4')
#To make them global:
color = ''
robot = False
ball = False
#Color values are hue values

while (cap.isOpened()):
    ret, frame = cap.read()
    
    #Check if cam read is successful
    if(ret):
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        #Red
        red_lower_hsv = np.array([90, 150, 130])
        red_upper_hsv = np.array([255, 255, 255])
        red = cv2.inRange(hsv, red_lower_hsv, red_upper_hsv) 

        #Blue
        blue_lower_hsv = np.array([90, 125, 104])
        blue_upper_hsv = np.array([160, 255, 255])
        blue = cv2.inRange(hsv, blue_lower_hsv, blue_upper_hsv) 

        #Green
        green_lower_hsv = np.array([30, 51, 91])
        green_upper_hsv = np.array([90, 255, 255])
        green = cv2.inRange(hsv, green_lower_hsv, green_upper_hsv)

        #robot
        robot_lower_hsv = np.array([0, 0, 0])
        robot_upper_hsv = np.array([40, 50, 50])
        robot = cv2.inRange(hsv, robot_lower_hsv, robot_upper_hsv)

        #Yellow ball
        yellow_lower_hsv = np.array([29, 86, 6])
        yellow_upper_hsv = np.array([64, 255, 255])
        yellow = cv2.inRange(hsv, yellow_lower_hsv, yellow_upper_hsv)

        #Sum colors
        greensum = np.sum(green)
        bluesum = np.sum(blue)
        redsum = np.sum(red)
        yellowsum = np.sum(yellow)
        robotsum = np.sum(robot)

        min = 5000
        minrobot = 10000


        #Check if we see a robot
        if(robotsum > min):
            robot = True
            #print("robot")
        
        if yellowsum > greensum and yellowsum > bluesum and yellowsum > redsum and yellowsum > min:
            #print("ball")
            ball = True

        if greensum > bluesum and greensum > redsum and greensum > min:
            #print("green")
            #print(greensum)
            color = 'green'
        elif bluesum > greensum and bluesum > redsum and bluesum > min:
            #print("blue")
            color = 'blue'
        elif redsum > greensum and redsum > bluesum and redsum > min:
            #print("red")
            color = 'red'

        k = cv2.waitKey(5) & 0xFF
        if k == 27:
            break

#Delete mp4 file
os.system("rm rec.mp4")
cv2.destroyAllWindows()
cap.release()