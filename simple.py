#!/bin/env python
#
# Program: Webcam read and output to virtual webcame.
# Auther: Hironobu SUZUKI <suzuki.hironobu@gmail.com>
# License: GPL v3 or later
# 2021-10-03
#
import sys
import os
import cv2
import math
import pyfakewebcam



vdev='/dev/video0'
height, width = 540,960
cam = cv2.VideoCapture(vdev)
if not cam.isOpened():
	print(vdev + " is not opened")
	sys.exit(1)
cam.set(cv2.CAP_PROP_FRAME_WIDTH ,width)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT,height)

## fake webcam
fake = pyfakewebcam.FakeWebcam('/dev/video20', width, height)

while True:
	stat,img = cam.read()
	if stat is False:
		cam.set(cv2.CAP_PROP_POS_FRAMES, 0)
		continue

	cv2.imshow('Cheating Webcam', img)
	frame = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
	fake.schedule_frame(frame)

	k = cv2.waitKey(1)
	if k & 0xFF == ord('q'): # ->Finish 
		break

cv2.destroyAllWindows()

