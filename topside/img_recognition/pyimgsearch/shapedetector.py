#!/usr/bin/python3
# -*- encoding: utf-8 -*-

import cv2

"""Reduce number of points representing curve using Ramer-Douglas-Peucker Algorithm or split-and-merge algorithm. Convert a curve to series of short line segments which becomes a subset of points defined by original curve. NOTE: Rectangle offset is corrected in detect_shapes.py"""
class ShapeDetector:
    count = {'tri': 0, 'sqr': 0, 'rct': -1, 'cir': 0}

    def __init__(self):
       pass
 
    def refresh_count(self):
        self.count = {'tri': 0, 'sqr': 0, 'rct': -1, 'cir': 0}

    def detect(self, c):
        # init shape name and approx contour
        shape = 'NaS'
        perimeter = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.04 * perimeter, True)

        # shape is triangle if 3 vertices
        if len(approx) == 3:
             shape = 'tri'
        # shape is square or rectangle if 4 vertices
        elif len(approx) == 4:
            # compute bounding box of contour and compute aspect ratio
            (x, y, w, h) = cv2.boundingRect(approx)
            ar = w / float(h)

            # square has aspect ratio close to 1 or else it is rectangle
            shape = 'sqr' if 0.90 <= ar <= 1.10 else 'rct'
        # shape is pentagon if 5 vertices
#        elif len(approx) == 5:
#            shape = 'pentagon'
        # otherwise assume shape is circle
        else:
            shape = 'cir'

        # keep count of identified shapes
        self.count[shape] += 1        

        # return name of shape
        return shape
