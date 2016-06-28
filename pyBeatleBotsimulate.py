from time import sleep
import videostream
import controller as j

import numpy as np
import imutils
import cv2


bit0Pin = 19
bit1Pin = 20
bit2Pin = 21
# Set up the GPIO channels

def main():

        bit0 = 0
        bit1 = 0
        bit2 = 0



        state = bytes(bit0) + bytes(bit1) + bytes(bit2)
        print(state)

        if bit2 == 0 and bit1 == 0 and bit0 == 0:
            print(" manaul")
            joy = j.Controller()
            joy.joystickControl()
        elif bit2 == 0 and bit1 == 0 and bit0== 1:
            print(" Automatic")
            v = videostream.vscreen()

            v.mainVideo()


        elif bit2 == 0 and bit1 == 1 and bit0 == 0:
            print("Tuin Point")
        elif bit2 == 0 and bit1 == 1 and bit0== 1:
            print(" Salt Point")


if __name__ == "__main__": main()



