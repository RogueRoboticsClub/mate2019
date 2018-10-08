#!/usr/bin/python3

import pygame
import robot_comm as ROV

pygame.init()
window = pygame.display.set_mode((800,600))
font = pygame.font.SysFont('Arial',20)
pygame.display.set_caption('Robot Control')
btns = [] #list of: (pygame.Rectangle button position, function to call when pressed)

lightStatus = False
def toggleLight(): #toggle Arduino's built in LED
    global lightStatus
    lightStatus = not lightStatus
    ROV.trySendCmd('on' if lightStatus else 'off')

def drawText(font,text,loc):
    window.blit(font.render(text,True,pygame.Color(0,0,0,255)),loc)
def drawBtn(font,text,loc,color,callback): #draw button and add to buttons list
    size = font.size(text)
    rect = pygame.Rect(loc[0],loc[1],size[0],size[1])
    pygame.draw.rect(window,color,rect)
    btns.append((rect,callback))
    drawText(font,text,loc)
def draw(): #full draw function; also generates list of buttons
    global btns
    btns = []
    window.fill(pygame.Color(255,255,255,255))
    if ROV.status == 'Connected': #main window
        drawText(font,'Robot Control',(0,0))
        drawText(font,'Status: '+ROV.status,(0,font.get_height()*1.5))
        drawBtn(font,'Example btn: toggle arduino light',(0,font.get_height()*3),pygame.Color(0,255,0,255),toggleLight)
    else: #connect button
        drawText(font,'Robot Control',(0,0))
        drawText(font,'Status: '+ROV.status,(0,font.get_height()*1.5))
        drawBtn(font,'Connect',(0,font.get_height()*3),pygame.Color(0,255,0,255),ROV.connectBackground)
    pygame.display.update()

def checkEvents(): #called every frame; checks for any inputs
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN: #key input example; left/right keys switch the light on/off
            if event.key == pygame.K_LEFT:
                ROV.trySendCmd('on')
            elif event.key == pygame.K_RIGHT:
                ROV.trySendCmd('off')
        elif event.type == pygame.MOUSEBUTTONDOWN: #check for button press and call a callback
            pos = event.dict['pos']
            for btn in btns:
                if pos[0] >= btn[0].left and pos[0] <= btn[0].right and pos[1] >= btn[0].top and pos[1] <= btn[0].bottom:
                    btn[1]()
                    break
        elif event.type == pygame.QUIT: #X button pressed
            quit()

def mainLoop(): #main loop repeated every frame
    draw()
    checkEvents()

while True:
    mainLoop()
