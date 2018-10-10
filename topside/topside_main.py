#!/usr/bin/python3

import pygame
import robot_comm as ROV
import speed_control as speed

windowSize = (1000,600) #TODO: make this scale for different screen sizes?
pygame.init()
window = pygame.display.set_mode(windowSize)
font = pygame.font.SysFont('Arial',20) #main font
pygame.display.set_caption('Rogue Robotics ROV Control')
btns = [] #list of: (pygame.Rectangle button position, function to call when pressed)
buttonClickPos = (0,0) #set when someone clicks a button; the click's position relative to the button's corner
camServoPosition = 0 #current position of camera servo

backgroundColor = pygame.Color(255,255,255,255)
textColor = pygame.Color(0,0,0,255)
errorTextColor = pygame.Color(255,0,0,255)
buttonColor = pygame.Color(0,255,0,255)
sliderForegroundColor = pygame.Color(0,0,0,255)
immovableSliderBackgroundColor = pygame.Color(0,255,0,255)
movableSliderBackgroundColor = pygame.Color(0,255,255,255)

lightStatus = False
def toggleLight(): #toggle Arduino's built in LED
    global lightStatus
    lightStatus = not lightStatus
    ROV.trySendCmd('on' if lightStatus else 'off')

def setBuoyancySetting(num): #returns a func that, when called, uses the buttonClickPos value to update buoyancy settings; this is used for the settings sliders
    return lambda: speed.setBuoyancySetting(num,buttonClickPos[0]/100 - 1)
def setCameraServo(): #when the camera slider is clicked, this is called; it sets the position of the camera servo based on click position
    global camServoPosition
    camServoPosition = buttonClickPos[0]/100 - 1
    ROV.setSpeed(6,camServoPosition)

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
def drawCameraFeed(camNum,loc,size): #TODO: get the camera feed and draw it
    drawClickableRect(loc,size,pygame.Color(0,0,0,255),lambda:None)
    drawText(font,'Cam Feed '+str(camNum),loc,pygame.Color(255,255,255,255))
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
        drawSlider(camServoPosition,(xOffset+45,yOffset),(200,20),movableSliderBackgroundColor,setCameraServo)
        yOffset += 25
        drawText(font,'Orientation: TODO',(xOffset,yOffset)) #TODO: t-shaped orientation slider thing (I'll do this later)
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
def checkEvents(): #called every frame; checks for any inputs
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key in movementKeys:
                speed.updateDirection(movementKeys[event.key][0],movementKeys[event.key][1])
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

#TODO: add xbox control
def mainLoop(): #main loop repeated every frame
    draw()
    checkEvents()

while True:
    mainLoop()
