#!/usr/bin/python3
# -*- encoding: -*-

import cv2

class ShapeDetector:
    def __init__(self):
        pass


"""
Reduce number of points representing curve using Ramer-Douglas-Peucker Algorithm or split-and-merge algorithm. Convert a curve to series of short line segments which becomes a subset of points defined by original curve.
"""
    def detect(self, c):
        # init shape name and approx contour
        shape = 'unidentified'
        perimeter = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.04 * peri, True)

        # shape is triangle if 3 vertices
        if len(approx) == 3:
            shape = 'triangle'
        # shape is square or rectangle if 4 vertices
        elif len(approx) == 4:
            # compute bounding box of contour and compute aspect ratio
            (x, y, w, h) = cv2.boundingRect(approx)
            ar = w / float(h)

            # square has aspect ratio close to 1 or else it is rectangle
            shape = 'square' if 0.95 <= ar <= 1.05 else 'rectangle'
        # shape is pentagon if 5 vertices
        elif len(approx) == 5:
            shape = 'pentagon'
        # otherwise assume shape is circle
        else:
            shape = 'circle'

        # return name of shape
        return shape
    
