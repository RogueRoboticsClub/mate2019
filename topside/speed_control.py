#!/usr/bin/python3

#TODO: calc_thrusts.py here

import robot_comm as ROV
import random
from math import copysign, sqrt

motors = [0,0,0,0,0,0,0] #motors 1-6; all values from -1 to 1
directionInputted = [0,0,0,0,0] #L/R;Fwd/Back;U/D;Turn;Cam; all values from -1 to 1
buoyancySettings = [0,0,0] #baseline settings for: pitch;roll;vertical; all values from -1 to 1

def updateMotors(mots): #update motors to a new list of motors
    global motors
    anyDifferent = False
    for i in range(len(mots)):
        if mots[i] != motors[i]:
            anyDifferent = True
    ROV.setSpeeds(mots)
    motors = mots

def adjustVal(x):
    return copysign(sqrt(abs(x)) / sqrt(3), x)

def calculateNewMotorSpeeds(): #calculate new motor speeds, and call updateMotors with the speeds
    mots = [0,0,0,0,0,0,0] #TODO: do some quick maths and calculate motor speeds; below is some BS fake math
    mots[0] = adjustVal(buoyancySettings[0]+buoyancySettings[1]+buoyancySettings[2])
    mots[1] = adjustVal(buoyancySettings[0]+buoyancySettings[1]-buoyancySettings[2])
    mots[2] = adjustVal(-buoyancySettings[0]+buoyancySettings[1]+buoyancySettings[2])
    mots[3] = adjustVal(-buoyancySettings[0]+buoyancySettings[1]-buoyancySettings[2])
    mots[4] = directionInputted[2]
    mots[5] = directionInputted[2]
    mots[6] = directionInputted[2]
    updateMotors(mots)
def updateDirection(directionNumber,val): #update which direction you want to move; updates motors accordingly
    global directionInputted
    if val >= -1 and val <= 1:
        directionInputted[directionNumber] = val
def setBuoyancySetting(setting,val): #set a new buoyancy setting; updates motors accordingly
    buoyancySettings[setting] = val #TODO: save buoyancy settings in a file so you don't have to figure them out every time?
    calculateNewMotorSpeeds()
