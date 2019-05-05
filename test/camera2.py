#!/usr/bin/python2

import pygame
import pygame.camera
import sys
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-p', '--port', type=str, default="/dev/ttyUSB0", help="arduino serial port")
parser.add_argument('-t', '--no-arduino', action="store_true", help="test without arduino")
parser.add_argument('-v', '--video', type=str, default='/dev/video2', help="video card")
args = parser.parse_args()

pygame.init()
pygame.camera.init()

screen = pygame.display.set_mode((640, 480))
clock = pygame.time.Clock()

camlist = pygame.camera.list_cameras()
if camlist:
	for camera in camlist:
		print(camera)

try:
    cam = pygame.camera.Camera(args.video, (640, 480))
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

wrist = 0
elbow = 0
prong = 0

def serv_constrain(x, dx):
    return min(255, max(x+dx, 0))

while True:
    # load the image and state text
    image = gi()
    image = pygame.transform.flip(image,True,False)
    screen.fill(BLACK)
    screen.blit(image, (0, 0))
    text = font.render('camera {}'.format(current_cam+1), True, RED)
    screen.blit(text, (20, 420))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # quit
            sys.exit(0)
        if event.type == pygame.KEYDOWN:
            print('-------------')
            print(event.unicode)


    current_cam %= NUM_CAMERAS

    pygame.display.flip()
    pygame.display.update()
clock.tick(20)

