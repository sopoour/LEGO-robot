import cv2
import numpy as np

cap = cv2.VideoCapture(0)

#Color values are hue values

while (1):
    _, frame = cap.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    #Red
    image_lower_hsv = np.array([150, 200, 220])
    image_upper_hsv = np.array([180, 255, 255])
    red1 = cv2.inRange(hsv, image_lower_hsv, image_upper_hsv)
    # 0 to 30
    image_lower_hsv = np.array([0, 200, 220])
    image_upper_hsv = np.array([10, 255, 255])
    red2 = cv2.inRange(hsv, image_lower_hsv, image_upper_hsv)
    # combine masks
    red = cv2.bitwise_or(red1, red2)

    #Blue
    blue_lower_hsv = np.array([90, 150, 220])
    blue_upper_hsv = np.array([130, 255, 255])
    blue = cv2.inRange(hsv, blue_lower_hsv, blue_upper_hsv) 

    # green
    green_lower_hsv = np.array([30, 100, 100])
    green_upper_hsv = np.array([80, 255, 255])
    green = cv2.inRange(hsv, green_lower_hsv, green_upper_hsv)

    #ball green/yellow

    # filder
    #kernel = np.ones((5, 5), np.uint8)
    #erosion = cv2.erode(finalMask, kernel, iterations=1)
    #smoothen = cv2.filter2D(finalMask, -1, kernel)
    #mask = cv2.inRange(hsv, lower_red, upper_red)
    #res = cv2.bitwise_and(frame, frame, mask=mask)

    cv2.imshow('frame', frame)
    #cv2.imshow('mask', mask)
    #cv2.imshow('res', res)
    cv2.imshow(' green',  green)
    cv2.imshow(' blue', blue)
    cv2.imshow('red', red)
    #cv2.imshow('smoothen', smoothen)
   # cv2.imshow('erosion', erosion)
    greensum=np.sum(green)
    bluesum=np.sum(blue)
    redsum=np.sum(red)
    min = 5000
    if greensum > bluesum and greensum > redsum and greensum > min:
        print("green")
        print(greensum)
    elif bluesum > greensum and bluesum > redsum and bluesum > min:
        print("blue")
    elif redsum > greensum and redsum > bluesum and redsum > min:
        print("red")
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()
cap.release()