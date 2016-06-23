
import numpy as np

import imutils
import cv2

cap = cv2.VideoCapture(0)
ret = cap.set(3,640)
ret = cap.set(4,480)

speedRight=200
speedLeft= 200
lastError = 0
integral = 0
Kp = 100
Kd = 100
Ki = 100
rightBaseSpeed = 100
leftBaseSpeed = 100
rightMaxSpeed = 250
leftMaxSpeed = 250
rightMotorSpeed = rightBaseSpeed
leftMotorSpeed = leftBaseSpeed

def speedSetter(error):
    lastError = error
    #nonlocal  integral , rightMotorSpeed, leftMotorSpeed
    #integral = integral + error
    derivative = error - lastError
    motorSpeed = Kp * error + Kd * derivative + integral * Ki
    rightMotorSpeed = rightBaseSpeed + motorSpeed;
    leftMotorSpeed = leftBaseSpeed - motorSpeed;
    
    if (rightMotorSpeed > rightMaxSpeed): rightMotorSpeed = rightMaxSpeed
    if (leftMotorSpeed > leftMaxSpeed): leftMotorSpeed = leftMaxSpeed
    if (rightMotorSpeed < 0): rightMotorSpeed = 0
    if (leftMotorSpeed < 0): leftMotorSpeed = 0


    
# load the image, convert it to grayscale, and blur it slightly
def vidFeed():
    ret, image = cap.read()
    height, width, channels = image.shape
    mask = np.zeros(image.shape, dtype=np.uint8)
    roi_corners = np.array([[(0, height * 0.25), ( 0 , height * 0.75) ,( width, height * 0.75) ,(width, height * 0.25)  ]], dtype=np.int32) #  ,(800, 200)
    centerFrameX = int(width /2)
    centerContoursX = int(width /2)
    channel_count = image.shape[2]  # i.e. 3 or 4 depending on your image
    ignore_mask_color = (255,) * channel_count
    cv2.fillPoly(mask, roi_corners, ignore_mask_color)


    # apply the mask
    masked_image = cv2.bitwise_and(image, mask)
    gray = cv2.cvtColor(masked_image, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    thresh = cv2.erode(thresh, None, iterations=2)
    thresh = cv2.dilate(thresh, None, iterations=2)

    cnts = cv2.findContours(thresh.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    if cnts is not None:
        cnts = cnts[0] if imutils.is_cv2() else cnts[1]
        c = max(cnts, key=cv2.contourArea)
        M = cv2.moments(c)
        cX = int((M["m10"] / M["m00"]) )
        cY = int((M["m01"] / M["m00"]) )

        #bounding Recatangle
        x, y, w, h = cv2.boundingRect(c)
        cv2.rectangle(image, (x, y), (x + w, y + h), (100, 100, 0), 2)

        #area Calculation checkpoint

        area = cv2.contourArea(c)
        cv2.putText(image, str(area), (width - 100, 50),cv2.FONT_HERSHEY_SIMPLEX,0.5, (255, 255, 255), 2)

        if(area > 140000):
            checkpoint = "REACHED"
        else:
            checkpoint = "NOT REACHED"

        cv2.putText(image, checkpoint, (width - 100, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

        #drawpoints of countours

        cv2.circle(image, (cX,cY), 6, (100, 200, 255), -1)  # red
        extLeft = tuple(c[c[:, :, 0].argmin()][0])
        extRight = tuple(c[c[:, :, 0].argmax()][0])
        extTop = tuple(c[c[:, :, 1].argmin()][0])
        extBot = tuple(c[c[:, :, 1].argmax()][0])

        centerContoursX = cX
        error = centerFrameX - centerContoursX
        if error > 0 :
            shape = "left"
        elif error < 0 :
            shape = "right"
        else :
            shape = " straight"

        cv2.putText(image, shape, (cX, cY), cv2.FONT_HERSHEY_SIMPLEX,
                        2, (255, 255, 255), 2)
        # draw the outline of the object, then draw each of the
        # extreme points, where the left-most is red, right-most
        # is green, top-most is blue, and bottom-most is teal
        cv2.line(image, (int(width /2) , 0  ), (int(width /2), height), (0, 255, 0), 2) #center line
        cv2.line(image, (0,int(height / 2)), (width, int(height / 2)), (0, 255, 0), 2)  # center line
        cv2.circle(image, (int(width/2), int(height/2)), 6, (200, 255, 0), -1)  # CenterPoint
        cv2.drawContours(image, [c], -1, (0, 255, 255), 2)
        cv2.circle(image, extLeft, 6, (0, 0, 255), -1)  # red
        cv2.circle(image, extRight, 6, (0, 255, 0), -1) # green
        cv2.circle(image, extTop, 6, (255, 0, 0), -1) # blue
        cv2.circle(image, extBot, 6, (255, 255, 0), -1) # bottom
    cv2.imshow("Image", image)
    cv2.imshow("blur", thresh)






