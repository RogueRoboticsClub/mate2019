#!/usr/bin/python3
# -*- encoding: utf-8 -*-

from pyimgsearch.shapedetector import ShapeDetector
# import argparse
import imutils
import cv2
import numpy as np 

# create ShapeDetector object
sd = ShapeDetector()

# construct terminal cmd arg parser
#ap = argparse.ArgumentParser()
#ap.add_argument('-i', '--image', required=True, help='path to the input image')
#args = vars(ap.parse_args())

def resize(image):
    # load and resize image to smaller factor for more effective approximations
    resized = imutils.resize(image, width=300)
    ratio = image.shape[0] / float(resized.shape[0])
    return (resized, ratio)

def process(image):
    # convert resized image to grayscale, blur it, and threshhold it
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    _, thresh = cv2.threshold(blurred, 70, 255, cv2.THRESH_BINARY)
    return thresh

def recognize_shapes(image, ratio, frame):
    # find contours in threshed image and initialize shape detector
    cnts = cv2.findContours(image.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    
    # loop through contours
    for c in cnts:
        # compute contours centers using moments and detect name of shape
        M = cv2.moments(c)
        if M["m00"] != 0:
            cX = int((M["m10"] / M["m00"]) * ratio)
            cY = int((M["m01"] / M["m00"]) * ratio)
            shape = sd.detect(c)
    
            # scale old coordinates to resized shape, then draw contours and name of shape on shape
            c = c.astype("float")
            c *= ratio
            c = c.astype("int")
            cv2.drawContours(frame, [c], -1, (0, 255, 0), 2)
            cv2.putText(frame, shape, (cX, cY), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    
    return frame

def draw_output(image):
    # get physical properties of frame
    height, width, channels = image.shape
    
    # draw bounding rectangle container for output
    cv2.rectangle(image, (width-100, 0), (width, 200), (255, 255, 0), thickness=cv2.FILLED)

    # draw triangle and output count
    points = np.array([[width-26, 20], [width-40, 50], [width-9, 50]], np.int32)
    points = points.reshape((3, 1, 2))
    cv2.fillPoly(image, [points], (0, 0, 255))
    cv2.putText(image, str(sd.count['tri']), (width-90, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), thickness=2, lineType=cv2.LINE_AA)

    # draw square and output count
    cv2.rectangle(image, (width-40, 60), (width-9, 90), (0, 0, 255), thickness=cv2.FILLED)
    cv2.putText(image, str(sd.count['sqr']), (width-90, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), thickness=2, lineType=cv2.LINE_AA)

    # draw rectangle and output count
    cv2.rectangle(image, (width-40, 110), (width-9, 120), (0, 0, 255), thickness=cv2.FILLED)
    cv2.putText(image, str(sd.count['rct']), (width-90, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), thickness=2, lineType=cv2.LINE_AA)

    # draw circle and output count
    cv2.circle(image, (width-24, 156), 16, (0, 0, 255), thickness=cv2.FILLED)
    cv2.putText(image, str(sd.count['cir']), (width-90, 161), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), thickness=2, lineType=cv2.LINE_AA)

    # refresh shapes count
    sd.refresh_count()

    return image
