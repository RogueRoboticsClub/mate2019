#!/usr/bin/python3

import pygame
import time
import datetime
import robot_comm as ROV
import speed_control as speed
import xbox_inp as xbox
from cameras import getCamNum, getNumOfCams

windowSize = (1000,600) #TODO: make this scale for different screen sizes?
pygame.init()
pygame.camera.init()
window = pygame.display.set_mode(windowSize)
font = pygame.font.SysFont('Arial',20) #main font
btns = [] #list of: (pygame.Rectangle button position, function to call when pressed)
buttonClickPos = (0,0) #set when someone clicks a button; the click's position relative to the button's corner

pygame.display.set_caption('Rogue Robotics ROV Control')
try:
    pygame.display.set_icon(pygame.image.load('Logo.png'))
except:
    try:
        pygame.display.set_icon(pygame.image.load('topside/Logo.png'))
    except:
        pass

backgroundColor = pygame.Color(255,255,255,255)
textColor = pygame.Color(0,0,0,255)
errorTextColor = pygame.Color(255,0,0,255)
buttonColor = pygame.Color(0,255,0,255)
sliderForegroundColor = pygame.Color(0,0,0,255)
immovableSliderBackgroundColor = pygame.Color(0,255,0,255)
movableSliderBackgroundColor = pygame.Color(0,255,255,255)

camNums = [-1,0]
cameras = [None, None]
def incrementCam(n):
    camNums[n] += 1
    camNums[n] %= getNumOfCams()
    cameras[n] = getCamNum(camNums[n], (340,300))

lightStatus = False
def toggleLight(): #toggle Arduino's built in LED
    global lightStatus
    lightStatus = not lightStatus
    ROV.trySendCmd('on' if lightStatus else 'off')

def setBuoyancySetting(num): #returns a func that, when called, uses the buttonClickPos value to update buoyancy settings; this is used for the settings sliders
    return lambda: speed.setBuoyancySetting(num,buttonClickPos[0]/100 - 1)
def setCameraServo(): #when the camera slider is clicked, this is called; it sets the position of the camera servo based on click position
    camServoPosition = buttonClickPos[0]/100 - 1
    speed.updateDirection(4,camServoPosition)

def drawText(font,text,loc,color = textColor): #draw text in given font
    window.blit(font.render(text,True,color),loc)
def drawClickableRect(loc,size,color,callback): #draw a rectangle and add to clickable buttons list
    rect = pygame.Rect(loc[0],loc[1],size[0],size[1])
    pygame.draw.rect(window,color,rect)
    btns.append((rect,callback))
def drawBtn(font,text,loc,color,callback): #draw button and add to buttons list
    drawClickableRect(loc,font.size(text),color,callback)
    drawText(font,text,loc)
def drawSlider(percent,loc,size,color,callback = (lambda: None)): #draw a slider with a given percentage (-1<p<1)
    drawClickableRect((loc[0],loc[1]+size[1]/4),(size[0],size[1]/2),color,callback)
    drawClickableRect((loc[0]+(size[0]*(.5+percent/2))-size[1]/2,loc[1]),(size[1],size[1]),sliderForegroundColor,callback)
def drawVerticalSlider(percent,loc,size,color,callback = (lambda: None)): #same as above but it's vertical (this function is only used once)
    drawClickableRect((loc[0]+size[0]/4,loc[1]),(size[0]/2,size[1]),color,callback)
    drawClickableRect((loc[0],loc[1]+(size[1]*(.5+percent/2))-size[0]/2),(size[0],size[0]),sliderForegroundColor,callback)
def drawCameraFeed(camNum,loc,size): #TODO: get the camera feed and draw it
    drawClickableRect(loc,size,pygame.Color(0,0,0,255),lambda:None)
    try:
        if cameras[camNum] != None and camNum < len(cameras) and cameras[camNum].query_image():
            img = cameras[camNum].get_image()
            img = pygame.transform.scale(img,size)
            window.blit(img, loc)
    except SystemError:
        pass
    drawText(font,'Cam Feed '+str(camNum+1),loc,pygame.Color(255,255,255,255))
def draw(): #full draw function; also generates list of buttons
    global btns
    btns = []
    window.fill(backgroundColor)

    ###THIRD COLUMN###
    xOffset = 650
    yOffset = 10
    drawCameraFeed(1,(xOffset,yOffset),(340,300))
    yOffset += 310
    drawText(font,'Controls:',(xOffset,yOffset))
    yOffset += font.get_height()*1.5
    drawText(font,'W/S: forward/back',(xOffset,yOffset))
    yOffset += font.get_height()*1
    drawText(font,'A/D: strafe left/right',(xOffset,yOffset))
    yOffset += font.get_height()*1
    drawText(font,'I/K: up/down',(xOffset,yOffset))
    yOffset += font.get_height()*1
    drawText(font,'J/L: turn',(xOffset,yOffset))
    yOffset += font.get_height()*1
    drawText(font,'1: switch cam view 1',(xOffset,yOffset))
    yOffset += font.get_height()*1
    drawText(font,'2: switch cam view 2',(xOffset,yOffset))
    yOffset += font.get_height()*1
    drawText(font,'Click blue sliders to adjust',(xOffset,yOffset))

    ###SECOND COLUMN###
    xOffset = 300
    yOffset = 10
    drawCameraFeed(0,(xOffset,yOffset),(340,300))
    yOffset += 310
    drawText(font,'Buoyancy:',(xOffset,yOffset))
    yOffset += font.get_height()*1.5
    drawText(font,'(These are added to the',(xOffset,yOffset))
    yOffset += font.get_height()*1
    drawText(font,'motor speeds, to account for',(xOffset,yOffset))
    yOffset += font.get_height()*1
    drawText(font,'buoyancy issues)',(xOffset,yOffset))
    yOffset += font.get_height()*1.5
    drawText(font,'Pitch',(xOffset,yOffset))
    drawSlider(speed.buoyancySettings[0],(xOffset+50,yOffset),(200,20),movableSliderBackgroundColor,setBuoyancySetting(0))
    yOffset += 25
    drawText(font,'Roll',(xOffset,yOffset))
    drawSlider(speed.buoyancySettings[1],(xOffset+50,yOffset),(200,20),movableSliderBackgroundColor,setBuoyancySetting(1))
    yOffset += 25
    drawText(font,'Vert.',(xOffset,yOffset))
    drawSlider(speed.buoyancySettings[2],(xOffset+50,yOffset),(200,20),movableSliderBackgroundColor,setBuoyancySetting(2))

    ###FIRST COLUMN###
    xOffset = 10
    yOffset = 10
    if ROV.status == 'Connected':
        drawText(font,'Uwe was here <3',(xOffset,yOffset))
        yOffset += font.get_height()*1.5
        drawText(font,'Status: '+ROV.status,(xOffset,yOffset))
        yOffset += font.get_height()*1.5
        drawBtn(font,'Toggle LED (testing)',(xOffset,yOffset),buttonColor,toggleLight)
        yOffset += font.get_height()*1.5
        for i in range(6):
            drawText(font,'M'+str(i+1),(xOffset,yOffset))
            drawSlider(speed.motors[i],(xOffset+45,yOffset),(200,20),immovableSliderBackgroundColor)
            yOffset += 25
        drawText(font,'Cam',(xOffset,yOffset))
        drawSlider(speed.directionInputted[4],(xOffset+45,yOffset),(200,20),movableSliderBackgroundColor,setCameraServo)
        yOffset += 25
        drawText(font,'Orientation:',(xOffset,yOffset))
        yOffset += font.get_height()
        drawVerticalSlider(.75,(xOffset+100,yOffset),(20,200),immovableSliderBackgroundColor) #TODO: ask ROV for its orientation (scale of -1 to 1) and show it here; replace .75 on this line and .5 on next
        drawSlider(.5,(xOffset+20/2,yOffset+100-20/2),(200,20),immovableSliderBackgroundColor)
        drawText(font,'Pitch',(xOffset+120,yOffset))
        drawText(font,'Roll',(xOffset,yOffset+100-20-font.get_height()))
    else:
        drawText(font,'Rogue Robotics ROV Control',(xOffset,0))
        yOffset += font.get_height()*1.5
        drawText(font,'Status: '+ROV.status,(xOffset,yOffset),errorTextColor)
        yOffset += font.get_height()*1.5
        drawBtn(font,'Connect',(xOffset,yOffset),buttonColor,ROV.connectBackground)

    pygame.display.update()

movementKeys = { #list of: key name -> (value in speed.directionInputted table, value aka +-1 )
    pygame.K_w: (1,1),
    pygame.K_s: (1,-1),
    pygame.K_d: (0,1),
    pygame.K_a: (0,-1),
    pygame.K_i: (2,1),
    pygame.K_k: (2,-1),
    pygame.K_l: (3,1),
    pygame.K_j: (3,-1)
}
xboxAxes = { #list of: axis num -> (value in speed.directionInputted table, multiplier, either -1 or 1)
    0: (0,1),
    1: (1,-1),
    3: (3,1),
    4: (2,-1)
}
updateCountdown = 0
def checkEvents(): #called every frame; checks for any inputs
    time.sleep(.1)
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key in movementKeys:
                speed.updateDirection(movementKeys[event.key][0],movementKeys[event.key][1])
            elif event.key == pygame.K_1:
                incrementCam(0)
            elif event.key == pygame.K_2:
                incrementCam(1)
        if event.type == pygame.KEYUP:
            if event.key in movementKeys:
                speed.updateDirection(movementKeys[event.key][0],0)
        elif event.type == pygame.MOUSEBUTTONDOWN: #check for button press and call a callback
            pos = event.dict['pos']
            for btn in btns:
                if pos[0] >= btn[0].left and pos[0] <= btn[0].right and pos[1] >= btn[0].top and pos[1] <= btn[0].bottom:
                    global buttonClickPos
                    buttonClickPos = (pos[0]-btn[0].left,pos[1]-btn[0].top)
                    btn[1]()
                    break
        elif event.type == pygame.QUIT: #X button pressed
            quit()
    inps = None
    try:
        inps = xbox.get_xbox_inps()
    except Exception as e: #TODO: error handling highkey doesnt work
        print(e)
    if inps != None: #TODO: if none connected, let the user know
        for axis,dir in xboxAxes.items():
            speed.updateDirection(dir[0],inps['axes'][axis]*dir[1])
        if inps['buttons'][4] == 1:
            speed.updateDirection(4, speed.directionInputted[4] - 0.05)
        if inps['buttons'][5] == 1:
            speed.updateDirection(4, speed.directionInputted[4] + 0.05)

    global updateCountdown
    updateCountdown -= 1
    if updateCountdown <= 0:
        if ROV.status == 'Connected':
            speed.calculateNewMotorSpeeds()
        updateCountdown = 5

#TODO: add xbox control
def mainLoop(): #main loop repeated every frame
    incrementCam(0)
    incrementCam(1)
    checkEvents()
    draw()

while True:
    mainLoop()
