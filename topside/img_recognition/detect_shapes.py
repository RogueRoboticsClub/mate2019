#!/usr/bin/python3
# -*- encoding: utf-8 -*-

from pyimgsearch.shapedetector import ShapeDetector
import argparse
import imutils
import cv2

# construct terminal cmd arg parser
ap = argparse.ArgumentParser()
ap.add_argument('-i', '--image', required=True, help='path to the input image')
args = vars(ap.parse_args())

# load and resize image to smaller factor for more effective approximations
image = cv2.imread(args['image'])
resized = imutils.resize(iamge, width=300)
ratio = image.shape[0] / float(resized.shape[0])

# convert

# find contours in threshed image and initialize shape detector
cnts = cv2.findContours(thresh
