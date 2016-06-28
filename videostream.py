import numpy as np
import imutils
import cv2


import serialArduino


class vscreen:


    def __init__(self):

        self.cap = cv2.VideoCapture(1)
        self.ret = self.cap.set(3,640)
        self.ret = self.cap.set(4,480)


    def takeFrame(self):
        self.ret, self.image = self.cap.read()



    def roiMask(self):
        mask = np.zeros(self.image.shape, dtype=np.uint8)
        roi_corners = np.array(
            [[(0, self.height * 0.25), (0, self.height * 0.75), (self.width, self.height * 0.75), (self.width, self.height * 0.25)]],
            dtype=np.int32)  # ,(800, 200)

        channel_count = self.image.shape[2]  # i.e. 3 or 4 depending on your image
        ignore_mask_color = (255,) * channel_count
        cv2.fillPoly(mask, roi_corners, ignore_mask_color)

        # apply the mask
        self.masked_image = cv2.bitwise_and(self.image, mask)


    def surveyFeed(self):
        self.takeFrame()

        self.height, self.width, self.channels = self.image.shape # get image dimension

        self.widthHalf =  int(self.width / 2)
        self.heightHalf = int(self.height / 2)
        self.centerFrameX =  int(self.width / 2)


    def vidFeed(self):


        self.takeFrame()

        # draw reference points and lines
        cv2.line(self.image, (self.widthHalf, 0), (self.widthHalf, self.height), (0, 255, 0), 2)  # center line
        cv2.line(self.image, (0, self.heightHalf), (self.width, self.widthHalf), (0, 255, 0), 2)  # center line
        cv2.circle(self.image, (self.widthHalf, self.heightHalf), 6, (200, 255, 0), -1)  # CenterPoint
        self.roiMask()

        # Process the image
        gray = cv2.cvtColor(self.masked_image, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (5, 5), 0)
        th = cv2.threshold(gray, 127,255, cv2.THRESH_BINARY )[1]
        th = cv2.erode(th, None, iterations=2)
        th = cv2.dilate(th, None, iterations=2)

        #finding the coutours from
        cnts = cv2.findContours(th.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

        self.thresh = th
        if cnts is not None:
            cnts = cnts[0] if imutils.is_cv2() else cnts[1]
            c = max(cnts, key=cv2.contourArea)
            self.rohitC = c
            #find the moments of image
            M = cv2.moments(c)
            self.cX = int((M["m10"] / M["m00"]) )
            self.cY = int((M["m01"] / M["m00"]) )

            #bounding Rectangle
            self.boux, self.bouy, self.bouw, self.bouh = cv2.boundingRect(c)
            cv2.rectangle(self.image, (self.boux, self.bouy), (self.boux + self.bouw, self.bouy + self.bouh), (100, 100, 0), 2)


            cv2.putText(self.image, str(self.boux) + str(" ") + str(self.bouy)  + str(" ")+ str(self.boux+self.bouw)  + str(" ")+ str(self.bouy+self.bouh), (self.width - 400, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (20, 255, 255), 2)

            #drawpoints of countours

            cv2.circle(self.image, (self.cX,self.cY), 6, (100, 200, 255), -1)  # red
            extLeft = tuple(c[c[:, :, 0].argmin()][0])
            extRight = tuple(c[c[:, :, 0].argmax()][0])
            extTop = tuple(c[c[:, :, 1].argmin()][0])
            extBot = tuple(c[c[:, :, 1].argmax()][0])

            centerContoursX = self.cX
            error = self.centerFrameX - centerContoursX
            print(error)
            self.control(error)
            # draw the outline of the object, then draw each of the
            # extreme points, where the left-most is red, right-most
            # is green, top-most is blue, and bottom-most is teal

            cv2.drawContours(self.image, [c], -1, (0, 255, 255), 2)
            cv2.circle(self.image, extLeft, 6, (0, 0, 255), -1)  # red
            cv2.circle(self.image, extRight, 6, (0, 255, 0), -1) # green
            cv2.circle(self.image, extTop, 6, (255, 0, 0), -1) # blue
            cv2.circle(self.image, extBot, 6, (255, 255, 0), -1) # bottom


    def showcase(self):
        cv2.imshow("Image", self.image)
        cv2.imshow("blur", self.thresh)



    def mainVideo(self):
        self.surveyFeed()
        sa = serialArduino.serialArduino()
        while True:
            self.vidFeed()
            self.showcase()

            if cv2.waitKey(1) & 0xFF == ord('q'):
               break


    def checkPoint(self):
        area = cv2.contourArea(self.rohitC)
        cv2.putText(self.image, str(area), (self.width - 100, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

        if (area > 140000):
            
            return 'c'
        else:
            if(self.bouw > 500):
                return 'r'
            else:
                return 'm'

        cv2.putText(self.image, checkpoint, (self.width - 100, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

    def control(self, error):
        sa = serialArduino.serialArduino()
        shape = "checkpoint"
        if (self.checkPoint() == 'm'):
            if error > 30:
                shape = "left"
                
                sa.sendChar('z')

            elif error < -30:
                shape = "right"
                
                sa.sendChar('c')
            else:
                shape = " straight"
                
                sa.sendChar('w')
        elif(self.checkPoint() == 'c' ):
            sa.sendChar('f')
            
            shape = "checkpoint"
        elif(self.checkPoint() == 'r' ):
            sa.sendChar('d')
            
            shape = "hard right"
        sa.readChar()
        print(shape)
        cv2.putText(self.image, shape, (self.cX, self.cY), cv2.FONT_HERSHEY_SIMPLEX,
                    2, (255, 255, 255), 2)

