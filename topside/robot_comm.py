#!/usr/bin/python3

import serial
import time

arduino = serial.Serial('/dev/ttyACM0',9600) #must change ttyACM0 each time; TODO: how to automatically find the arduino?

def waitForReady():
    while True:
        try:
            commandwithresponse('hi')
            return
        except:
            pass
        time.sleep(.1)
def readln():
    if arduino.inWaiting():
        return (arduino.readline()) #CODE THAT READS OVER SERIAL; previous line is necessary to prevent program from freezing
    else:
        return bytes()
def sendcmd(cmd,args=[]): #send command and wait for acknowledgement
    x = bytes(cmd,'utf8')+bytes(args)+bytes('\n','utf8')
    arduino.write(x)
    currentTime = time.clock()
    while time.clock()<currentTime+2: #2 seconds for it to acknowledge it recieved it; then it gives up
        if readln() == bytes('received: ','utf8')+x:
            return
    raise Exception('arduino never acknowledged command '+cmd)
def commandwithresponse(cmd,args=[]): #send command, get response, and returns it
    sendcmd(cmd,args)
    time.sleep(.01)
    return [x for x in readln()][:-1]

def startup():
    print('Waiting for Arduino connection...')
    waitForReady()
    print('Connected')
