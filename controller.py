import pygame
import serial
import signal
import sys
import threading
import io

ser = serial.Serial('/dev/ttyACM0', 19200, timeout=0.005)
sio = io.TextIOWrapper(io.BufferedRWPair(ser, ser))

class joystick():

    def __init___(self):
        pygame.joystick.init()
        pygame.display.init()
        if not pygame.joystick.get_count():
            print("\nPlease connect a joystick and run again.\n")
            quit()
        print("\n%d joystick(s) detected." % pygame.joystick.get_count())
        self._joy = pygame.joystick.Joystick(0)
        self._joy.init()

        print("Ready for Action\n")


    def printsioSerial(self):
        sio.flush()
        #data = sio.readline()  # the last bit gets rid of the new-line chars
        #if data:
        #	print (data)

    def joystickControl(self):
            buttons = self._joy.get_numbuttons()
            event = pygame.event.wait()
            if event.type == pygame.JOYBUTTONDOWN:
                if self._joy.get_button(0) == 1 :
                    print("forward")
                    sio.write(unicode('w'))
                if self._joy.get_button(2) == 1:
                    print("reverse")
                    sio.write(unicode('s'))
                if self._joy.get_button(3) == 1:
                    print ("left")
                    sio.write(unicode('a'))
                if self._joy.get_button(1) == 1:
                    print("right")
                    sio.write(unicode('d'))
                #servoBase
                if self._joy.get_button(4) == 1:
                    print("servobase increase")
                    sio.write(unicode('t'))
                if self._joy.get_button(6) == 1:
                    print("servobase decrease")
                    sio.write(unicode('g'))
                 #servoA and servo B
                if self._joy.get_button(5) == 1:
                    print("servoa increase")
                    sio.write(unicode('y'))
                if self._joy.get_button(7) == 1:
                    print("servoa decrease")
                    sio.write(unicode('h'))
                #tuin
                if self._joy.get_button(10) == 1:
                    print("Tuin grab")
                    sio.write(unicode('u'))
                if self._joy.get_button(11) == 1:
                    print("Tuin realease")
                    sio.write(unicode('j'))



            if event.type == pygame.JOYBUTTONUP:
                sio.write(unicode('f'))
                sio.write(unicode('n'))
            #printsioSerial()




