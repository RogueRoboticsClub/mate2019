#!/usr/bin/python3
# -*- encoding: utf-8 -*-

import numpy as np
import cv2
import imutils

cap = cv2.VideoCapture(0)

def process_img(frame):
    # convert frame to grayscale
    grayscale = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # add Gaussian blur
    blurred = cv2.GaussianBlur(grayscale, (5, 5), 0)
    # add threshold
    thresholded = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY)[1]

    return thresholded

def get_contours(processed):
    # returns sets of outlines that make up each thresholded object and grabs the corresponding tuple based on cv2 version
    cnts = cv2.findContours(processed.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    return cnts

while True:
    # split capture return values
    ret, frame = cap.read()
    # flip frame
    frame = cv2.flip(frame, 1)
    processed = process_img(frame)
    cnts = get_contours(processed)
    # iterate over each contour
    for c in cnts:
        # compute centroid of contours
        M = cv2.moments(c)
        if M['m00'] != 0:
            cX = int(M['m10'] / M['m00'])
            cY = int(M['m01'] / M['m00'])

        	# # draw the contour and center of the shape on the image
            # cv2.drawContours(processed, [c], -1, (0, 255, 0), 2)
            # cv2.circle(processed, (cX, cY), 7, (255, 255, 255), -1)
            # cv2.putText(processed, 'c', (cX - 20, cY - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

        	# draw the contour and center of the shape on the image
            cv2.drawContours(frame, [c], -1, (0, 255, 0), 2)
            cv2.circle(frame, (cX, cY), 7, (255, 255, 255), -1)
            cv2.putText(frame, 'c', (cX - 20, cY - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

    # show stream
    cv2.imshow('stream', frame)
    # quit stream
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
