#!/usr/bin/python3

import serial
import time

arduino = serial.Serial('/dev/ttyACM0',9600) #must change ttyACM0 each time; TODO: how to automatically find the arduino?

while True:
    if arduino.inWaiting():
        print(arduino.readline()) #CODE THAT READS OVER SERIAL; previous line is necessary to prevent program from freezing
    x = bytes(input()+'\n','utf8') #take command input and convert to bytes
    arduino.write(x) #CODE THAT WRITES OVER SERIAL
    time.sleep(.1)
