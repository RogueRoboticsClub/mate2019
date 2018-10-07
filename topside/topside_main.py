#!/usr/bin/python3

import pygame
import robot_comm

pygame.init()
window = pygame.display.set_mode((800,600))
pygame.font.init()
font = pygame.font.SysFont("Arial",50)

def drawText(font,text,loc):
    window.blit(font.render(text,True,pygame.Color(0,0,0,255)),loc)
def draw():
    window.fill(pygame.Color(255,255,255,255))
    pygame.draw.rect(window,pygame.Color(0,255,255,255),pygame.Rect(0,0,100,200))
    drawText(font,"Rogue Underwater Solutions",(0,0))
    pygame.display.update()

def checkEvents():
    for event in pygame.event.get():
        print(event)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                robot_comm.sendcmd("on")
            elif event.key == pygame.K_RIGHT:
                robot_comm.sendcmd("off")
        elif event.type == pygame.QUIT:
            quit()

while True:
    draw()
    checkEvents()
