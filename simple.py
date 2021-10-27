#!/bin/env python
#
# Program: Webcam read and output to virtual webcame.
# Auther: Hironobu SUZUKI <suzuki.hironobu@gmail.com>
# License: GPL v3 or later
# Date: 2021-10-03
# Last: 2021-10-28
#
import sys
import os
import cv2
import math
import pyfakewebcam

vdev='/dev/video0'
args = sys.argv
if  len(args) > 1  :
	vdev=args[1]


print(vdev)
height, width = 540,960
cam = cv2.VideoCapture(vdev)
if not cam.isOpened():
	print(vdev + " is not opened")
	sys.exit(1)
cam.set(cv2.CAP_PROP_FRAME_WIDTH ,width)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT,height)
W = int(cam.get(cv2.CAP_PROP_FRAME_WIDTH))
H = int(cam.get(cv2.CAP_PROP_FRAME_HEIGHT))
if int((W/H)*1000) != int((width/height)*1000):
	print("Camera must support 16:9 aspect ratio:", W,H)
	sys.exit(1)


## fake webcam
fake = pyfakewebcam.FakeWebcam('/dev/video20', width, height)

while True:
	stat,img = cam.read()
	if stat is False:
		cam.set(cv2.CAP_PROP_POS_FRAMES, 0)
		continue

	cv2.imshow('Cheating Webcam', img)
	frame = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
	resizedFrame = cv2.resize(frame, (width,height))
	fake.schedule_frame(resizedFrame)

	k = cv2.waitKey(1)
	if k & 0xFF == ord('q'): # ->Finish 
		break

cv2.destroyAllWindows()

