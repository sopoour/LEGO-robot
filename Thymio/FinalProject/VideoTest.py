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
#Color 0 = Red, 1 = Green, 2 = Blue
color = 0
robot = False
#ball = False
#Color values are hue values

# 3 = Left, 2 = Straight, 1 = Right
direction = 0
# True = Short, False = Long
distance = False
    
# Crop picture left, middle, right, short, long
xLeftMin = 0
xLeftMax = 213

xMiddleMin = 214
xMiddleMax = 427

xRightMin = 428
xRightMax = 640

yShort = 0
yMedium = 240
yLong = 480

cv2.namedWindow("LeftShort")
cv2.namedWindow("LeftLong")
cv2.namedWindow("MiddleShort")
cv2.namedWindow("MiddleLong")
cv2.namedWindow("RightShort")
cv2.namedWindow("RightLong")

while (cap.isOpened()):
    ret, frame = cap.read()
    
    #Check if cam read is successful
    if(ret):	
		#Splitting the image in six parts
        longLeft = frame[yShort:yMedium,xLeftMin:xLeftMax]
        longMiddle = frame[yShort:yMedium,xMiddleMin:xMiddleMax]
        longRight = frame[yShort:yMedium,xRightMin:xRightMax]
        shortLeft = frame[yMedium:yLong,xLeftMin:xLeftMax]
        shortMiddle = frame[yMedium:yLong,xMiddleMin:xMiddleMax]
        shortRight = frame[yMedium:yLong,xRightMin:xRightMax]
		
        hsvLongLeft = cv2.cvtColor(longLeft, cv2.COLOR_BGR2HSV)
        hsvLongMiddle = cv2.cvtColor(longMiddle, cv2.COLOR_BGR2HSV)
        hsvLongRight = cv2.cvtColor(longRight, cv2.COLOR_BGR2HSV)
        hsvShortLeft = cv2.cvtColor(shortLeft, cv2.COLOR_BGR2HSV)
        hsvShortMiddle = cv2.cvtColor(shortMiddle, cv2.COLOR_BGR2HSV)
        hsvShortRight = cv2.cvtColor(shortRight, cv2.COLOR_BGR2HSV)
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

        min = 5000
        minrobot = 10000

        #cv2.imshow('frame', frame)
        cv2.imshow("LeftShort", shortLeft)
        cv2.imshow("LeftLong", longLeft)
        cv2.imshow("MiddleShort", shortMiddle)
        cv2.imshow("MiddleLong", longMiddle)
        cv2.imshow("RightShort", shortRight)
        cv2.imshow("RightLong", longRight)

        print("yellowsumShortLeft", yellowsumShortLeft)
        print("yellowsumShortMiddle", yellowsumShortMiddle)
        print("yellowsumShortRight", yellowsumShortRight)
        print("yellowsumLongLeft", yellowsumLongLeft)
        print("yellowsumLongMiddle", yellowsumLongMiddle)
        print("yellowsumLongRight", yellowsumLongRight)

        #Check if we see a robot
        if(robotsumLongLeft > min or robotsumLongMiddle > min or robotsumLongRight > min):
            robot = True
            print("robot")
        
        if yellowsumShortLeft > min and yellowsumShortLeft > yellowsumShortMiddle and yellowsumShortLeft > yellowsumShortRight and yellowsumShortLeft > yellowsumLongLeft and yellowsumShortLeft > yellowsumLongMiddle and yellowsumShortLeft > yellowsumLongRight:
            print("yellowsumShortLeft")
            direction = 3
            distance = True

        elif yellowsumShortMiddle > min and yellowsumShortMiddle > yellowsumShortLeft and yellowsumShortMiddle > yellowsumShortRight and yellowsumShortMiddle > yellowsumLongLeft and yellowsumShortMiddle > yellowsumLongMiddle and yellowsumShortMiddle > yellowsumLongRight:
            print("yellowsumShortMiddle")
            direction = 2
            distance = True
        
        elif yellowsumShortRight > min and yellowsumShortRight > yellowsumShortLeft and yellowsumShortRight > yellowsumShortMiddle and yellowsumShortRight > yellowsumLongLeft and yellowsumShortRight > yellowsumLongMiddle and yellowsumShortRight > yellowsumLongRight:
            print("yellowsumShortRight")
            direction = 1
            distance = True

        elif yellowsumLongLeft > min and yellowsumLongLeft > yellowsumShortLeft and yellowsumLongLeft > yellowsumShortMiddle and yellowsumLongLeft > yellowsumShortRight and yellowsumLongLeft > yellowsumLongMiddle and yellowsumLongLeft > yellowsumLongRight:
            print("yellowsumLongLeft")
            direction = 3
            distance = False
        
        elif yellowsumLongMiddle > min and yellowsumLongMiddle > yellowsumShortLeft and yellowsumLongMiddle > yellowsumShortMiddle and yellowsumLongMiddle > yellowsumShortRight and yellowsumLongMiddle > yellowsumLongLeft and yellowsumLongMiddle > yellowsumLongRight:
            print("yellowsumLongMiddle")
            direction = 2
            distance = False
        
        elif yellowsumLongRight > min and yellowsumLongRight > yellowsumShortLeft and yellowsumLongRight > yellowsumShortMiddle and yellowsumLongRight > yellowsumShortRight and yellowsumLongRight > yellowsumLongLeft and yellowsumLongRight > yellowsumLongMiddle:
            print("yellowsumLongRight")
            direction = 1
            distance = False

        print("direction", direction)
        print(distance)
        #if greensum > bluesum and greensum > redsum and greensum > min:
            #print("green")
            #print(greensum)
         #   color = 'green'
        #elif bluesum > greensum and bluesum > redsum and bluesum > min:
            #print("blue")
        #    color = 'blue'
        #elif redsum > greensum and redsum > bluesum and redsum > min:
            #print("red")
         #   color = 'red'

        k = cv2.waitKey(5) & 0xFF
        if k == 27:
            break

#Delete mp4 file
os.system("rm rec.mp4")
cv2.destroyAllWindows()
cap.release()