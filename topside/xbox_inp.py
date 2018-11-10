#!/usr/bin/python3

import pygame

pygame.init()
pygame.joystick.init()
def get_joystick():
    numJoysticks = pygame.joystick.get_count()
    if (numJoysticks != 1):
        return None
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    return joystick
def get_xbox_inps():
    joystick = get_joystick()
    if joystick == None: return None
    if (joystick.get_name() != "Xbox 360 Wireless Receiver (XBOX)"):
        raise Exception("Xbox 360 controller required")
    axes = [joystick.get_axis(i) for i in range(joystick.get_numaxes())]
    buttons = [joystick.get_button(i) for i in range(joystick.get_numbuttons())]
    hat = joystick.get_hat(0)
    return {"axes":axes,"buttons":buttons,"hat":hat}
