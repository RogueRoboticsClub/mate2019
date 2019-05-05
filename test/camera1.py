#!/usr/bin/python2

import pygame
import pygame.camera
import sys
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-v', '--video', type=str, default='/dev/video1', help="video card")
args = parser.parse_args()

pygame.init()
pygame.camera.init()

screen = pygame.display.set_mode((900, 1600))
clock = pygame.time.Clock()

camlist = pygame.camera.list_cameras()
if camlist:
	for camera in camlist:
		print(camera)

try:
    cam = pygame.camera.Camera(args.video, (1200, 1200))
    cam.start()
    gi = lambda: cam.get_image()
except Exception as e:
    img = pygame.image.load('blah.png')
    gi = lambda: img


NUM_CAMERAS = 4
current_cam = 0
font = pygame.font.Font(None, 20)
RED = (255, 0, 0)
BLACK = (0, 0, 0)



while True:
    # load the image and state text
    image = gi()
    image = pygame.transform.flip(image,True,False)
    image = pygame.transform.rotate(image,90)
    #screen.fill(BLACK)
    screen.blit(image, (0, 0))
    text = font.render('camera {}'.format(current_cam+1), True, RED)
    screen.blit(text, (20, 420))


    current_cam %= NUM_CAMERAS

    pygame.display.flip()
    pygame.display.update()
clock.tick(20)

