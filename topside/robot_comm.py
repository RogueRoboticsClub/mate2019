#!/usr/bin/python3

import serial
import serial.tools.list_ports
import time
import threading

arduino = None
status = 'Not started'

def waitForReady():
    attempts = 1
    while True:
        try:
            commandWithResponse('hi')
            return
        except:
            pass
        attempts += 1
        if attempts > 5:
            global status
            status = 'Failed to connect'
            raise Exception('Failed to connect')
        time.sleep(.1)
def readLn():
    if arduino.inWaiting():
        return (arduino.readline()) #CODE THAT READS OVER SERIAL; previous line is necessary to prevent program from freezing
    else:
        return bytes()
def sendCmd(cmd,args=[]): #send command and wait for acknowledgement
    x = bytes(cmd,'utf8')+bytes(args)+bytes('\n','utf8')
    arduino.write(x)
    currentTime = time.clock()
    while time.clock()<currentTime+2: #2 seconds for it to acknowledge it recieved it; then it gives up
        if readLn() == bytes('received: ','utf8')+x:
            return
    raise Exception('Arduino never acknowledged command: '+cmd)
def commandWithResponse(cmd,args=[]): #send command, get response, and returns it
    sendCmd(cmd,args)
    time.sleep(.01)
    return [x for x in readLn()][:-1]
def trySendCmd(cmd,args=[]): #tries to send a command; if it fails, it updates status
    global status
    try:
        sendCmd(cmd,args)
    except serial.serialutil.SerialException:
        status = 'Arduino disconnected'
    except Exception as e:
        status = 'Error: '+str(e)
def tryCommandWithResponse(cmd,args=[]): #tries to send a command with a response; if it fails, it updates status
    global status
    try:
        return commandWithResponse(cmd,args)
    except serial.serialutil.SerialException:
        status = 'Arduino disconnected'
    except Exception as e:
        status = 'Error: '+str(e)
    return bytes()
def setSpeeds(speeds):
    table = []
    for speed in speeds:
        table += [x for x in int.to_bytes(int(speed*400)+1500,2,byteorder='big')]
    trySendCmd('speeds',table)
def getPort(): #get the port associated with Arduino
    ports = serial.tools.list_ports.comports()
    for p in ports:
        if p.manufacturer.find('Arduino') != -1:
            return p.device
    global status
    status = 'No Arduino found'
    raise Exception('No Arduino found')
def connect(): #connect to Arduino
    global arduino
    global status
    try:
        arduino = serial.Serial(getPort(),9600)
    except Exception as e:
        status = 'Error: '+str(e)
        return
    status = 'Connecting...'
    waitForReady()
    status = 'Connected'
def connectBackground(): #connect in the background, allowing other processes to run in the meantime
    global status
    if status != 'Connecting...':
        threading.Thread(target=connect).start()
