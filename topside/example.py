#!/usr/bin/python3

import serial

arduino = serial.Serial('/dev/ttyACM2',9600)

print("starting")
while True:
    if arduino.inWaiting():
        print(arduino.readline())
    x = input()
    arduino.write(bytes(x,'utf8'))
print("done")
