#!/usr/bin/python3

import pygame
import pygame.camera

pygame.init()
pygame.camera.init()

camerasLoaded = {}

def getCam(name, size):
    global camerasLoaded
    if name in camerasLoaded:
        cam = camerasLoaded[name]
        try:
            if cam.query_image(): cam.get_image()
        except SystemError:
            del camerasLoaded[name]
        return cam
    else:
        cam = pygame.camera.Camera(name, size)
        try:
            cam.start()
        except SystemError:
            pass
        camerasLoaded[name] = cam
        return cam

def getCams(size):
    camlist1 = pygame.camera.list_cameras()
    camlist2 = camlist1[-2:] # there are only 2 cameras so the last 2 cameras on the list are probably right
    print(camlist2)
    camlist3 = map(lambda x: getCam(x, size), camlist2)
    return list(camlist3)
