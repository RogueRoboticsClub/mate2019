#!/usr/bin/python3
# -*- encoding: utf-8 -*-

import cv2
import detect_shapes

# create VideoCapture object
cap = cv2.VideoCapture(0)

while True:
    # split capture return values
    ret, frame = cap.read()

    # flip frame
    frame = cv2.flip(frame, 1)   
 
    # resize frame and obtain ratio
    resized, ratio = detect_shapes.resize(frame)

    # process image
    thresh = detect_shapes.process(resized)

    # find, classify, and draw contours/shapes on images
    frame = detect_shapes.recognize_shapes(thresh, ratio, frame)
    
    # draw output to final
    final = detect_shapes.draw_output(frame)

    # show image stream
    cv2.imshow("Thresh", thresh)
    cv2.imshow("Image", final)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
