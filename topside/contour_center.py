#!/usr/bin/python3
# -*- encoding: utf-8 -*-

import argparse
import cv2
import imutils

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument('-i', '--image', required=True, help='shapes_fodder.jpg')
args = vars(ap.parse_args())

# load the image, convert it to grayscale, blur it slightly, and threshold it
image = cv2.imread(args['image'])
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (5, 5), 0)
thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY)[1]

# returns sets of outlines that make up each thresholded object and grabs the corresponding tuple based on cv2 version
cnts1 = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts1)

print(cnts1)


# iterate over each contour
for c in cnts:
    # compute centroid of contours
    M = cv2.moments(c)
    if M['m00'] != 0:
        cX = int(M['m10'] / M['m00'])
        cY = int(M['m01'] / M['m00'])

    	# draw the contour and center of the shape on the image
        cv2.drawContours(image, [c], -1, (0, 255, 0), 2)
        cv2.circle(image, (cX, cY), 7, (255, 255, 255), -1)
        cv2.putText(image, 'c', (cX - 20, cY - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

# shows image and closes on 'q' press
while True:
    cv2.imshow('image', image)
    if cv2.waitKey(0) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
