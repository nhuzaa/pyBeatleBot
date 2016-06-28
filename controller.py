import pygame
import serialArduino


class Controller:

    def __init__(self):
        pygame.joystick.init()
        pygame.display.init()
        if not pygame.joystick.get_count():
            print("\nPlease connect a joystick and run again.\n")
            quit()
        print("\n%d joystick(s) detected." % pygame.joystick.get_count())
        self.joy = pygame.joystick.Joystick(0)
        self.joy.init()
        print("Ready for Action\n")

    def joystickControl(self):
        sa = serialArduino.serialArduino()
        while True:
            event = pygame.event.wait()
            if event.type == pygame.JOYBUTTONDOWN:
                if self.joy.get_button(0) == 1 :
                    print("forward")
                    sa.sendChar('w')
                if self.joy.get_button(2) == 1:
                    print("reverse")
                    sa.sendChar('s')
                if self.joy.get_button(3) == 1:
                    print ("left")
                    sa.sendChar('a')
                if self.joy.get_button(1) == 1:
                    print("right")
                    sa.sendChar('d')
                #servoBase
                if self.joy.get_button(4) == 1:
                    print("servobase increase")
                    sa.sendChar('t')
                if self.joy.get_button(6) == 1:
                    print("servobase decrease")
                    sa.sendChar('g')
                 #servoA and servo B
                if self.joy.get_button(5) == 1:
                    print("servoa increase")
                    sa.sendChar('y')
                if self.joy.get_button(7) == 1:
                    print("servoa decrease")
                    sa.sendChar('h')
                #tuin
                if self.joy.get_button(10) == 1:
                    print("Tuin grab")
                    sa.sendChar('u')
                if self.joy.get_button(11) == 1:
                    print("Tuin realease")
                    sa.sendChar('j')



            if event.type == pygame.JOYBUTTONUP:
                sa.sendChar('f')
                sa.sendChar('n')

            sa.readChar();


