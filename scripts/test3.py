#!/usr/bin/env python3
import rospy
import core
import cv2
import numpy as np
import time

rospy.init_node('asdf')
rospy.loginfo('asdf node started')
hccd = core.neural_networks.HCCD()

colors = {'red': (0, 0, 255), 'yellow': (0, 255, 255), 'green': (0, 255, 0)}

cap = cv2.VideoCapture(0)
while cap.isOpened():
    success, frame = cap.read()
    if not success:
        continue
    results = hccd.process(frame)
    for result in results:
        cv2.rectangle(frame, (result.left, result.top), (result.right, result.bottom), colors[result.class_name], 2)
        cv2.putText(frame, result.class_name, (result.left, result.top), cv2.FONT_HERSHEY_SIMPLEX, 1,
                    colors[result.class_name], 2)
    cv2.imshow('frame', frame)
    key = cv2.waitKey(16)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()