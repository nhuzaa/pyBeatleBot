import RPi.GPIO as GPIO
from time import sleep
import videostream
import controller
import wiringPi
from threading import Thread


GPIO.setmode(GPIO.BCM)
bit0Pin = 19
bit1Pin = 20
bit2Pin = 21
# Set up the GPIO channels
GPIO.setup(bit0Pin, GPIO.IN,pull_up_down=GPIO.PUD_DOWN) # This could be used to detect a switch
GPIO.setup(bit1Pin, GPIO.IN,pull_up_down=GPIO.PUD_DOWN) # This is going to supply the on/off signal
GPIO.setup(bit2Pin, GPIO.IN,pull_up_down=GPIO.PUD_DOWN) # This could be used to detect a switch

bit0 = GPIO.input(bit0Pin)
bit1 = GPIO.input(bit1Pin)
bit2 = GPIO.input(bit2Pin)


def main():
    while True:
        # Input from pin 11


        if bit0 == 0:
            print(" manaul")
            #controller.joystick.joystickControl()
        else:

            print(" Automatic")
            #videostream.vidFeed()

def checkButton():

    global bit0
    global bit1
    global bit2
    bit0 = GPIO.input(bit0Pin)
    bit1 = GPIO.input(bit1Pin)
    bit2 = GPIO.input(bit2Pin)


if __name__ == "__main__":
    Thread(target=main()).start()
    Thread(target=checkButton).start()