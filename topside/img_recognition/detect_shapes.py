#!/usr/bin/python3
# -*- encoding: utf-8 -*-

from pyimgsearch.shapedetector import ShapeDetector
# import argparse
import imutils
import cv2 

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
    thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY)[1]
    return thresh

def recognize_shapes(image, ratio, frame):
    # find contours in threshed image and initialize shape detector
    cnts = cv2.findContours(image.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
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
    
    # draw shapes and count output
#    cv2.(image, (width-40, 10), (width-10, 40), (0, 0, 255), thickness=cv2.FILLED)
#    cv2.putText(image, str(sd.count['tri']), (width-90, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), thickness=2, lineType=cv2.LINE_AA)
    cv2.rectangle(image, (width-40, 40), (width-9, 70), (0, 0, 255), thickness=cv2.FILLED)
    cv2.putText(image, str(sd.count['sqr']), (width-90, 65), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), thickness=2, lineType=cv2.LINE_AA)
    cv2.rectangle(image, (width-40, 90), (width-9, 100), (0, 0, 255), thickness=cv2.FILLED)
    cv2.putText(image, str(sd.count['rct']), (width-90, 105), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), thickness=2, lineType=cv2.LINE_AA)
    cv2.circle(image, (width-24, 136), 16, (0, 0, 255), thickness=cv2.FILLED)
    cv2.putText(image, str(sd.count['cir']), (width-90, 145), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), thickness=2, lineType=cv2.LINE_AA)

    # reset shapes count
    sd.reset_count()

    return image
