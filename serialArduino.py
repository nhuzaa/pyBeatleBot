import serial
import io


class serialArduino:
    def __init__(self):
        serSpeed = 57600
        try:
            ser = serial.Serial('/dev/ttyACM0', serSpeed, timeout=0.005)
        except:
            try:
                ser = serial.Serial('/dev/ttyACM1', serSpeed, timeout=0.005)
            except:
                    try:
                        ser = serial.Serial('/dev/ttyACM2', serSpeed, timeout=0.005)
                    except:
                        try:
                            ser = serial.Serial('/dev/ttyACM3', serSpeed, timeout=0.005)
                        except:
                            try:
                                ser = serial.Serial('/dev/ttyACM4', serSpeed, timeout=0.005)
                            except:
                                ser = serial.Serial('/dev/ttyACM5', serSpeed, timeout=0.005)


        self.sio = io.TextIOWrapper(io.BufferedRWPair(ser, ser))

    def sendChar(self, c):
        self.sio.write(unicode(c))

    def readChar(self):
        self.sio.flush()
        data = self.sio.readline()  # the last bit gets rid of the new-line chars
        if data:
        	print (data)

