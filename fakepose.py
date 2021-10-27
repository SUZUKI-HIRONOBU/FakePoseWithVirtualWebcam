#!/bin/env python
#
# Program: Webcam read and output to virtual webcame.
# Auther: Hironobu SUZUKI <suzuki.hironobu@gmail.com>
# License: GPL v3 or later
# Date: 2021-10-03
#
import sys
import os
import cv2
import math
import pyfakewebcam

vdev='/dev/video0'

args = sys.argv
if [ args[1] != None ] :
	vdev=args[1]


v4l2=True
fakeimg=None

### for circle
cl=[8,16,24,32,40,48,56,64,72,80,88,96,104,112,120,128,136,144,152,160,168,176,184,192,200,208,216,224,232,255]


height, width = 540,960			# This size depends on Fake Webcam
cam = cv2.VideoCapture(vdev)
if not cam.isOpened():
	print(vdev + " is not opened")
	sys.exit(1)
cam.set(cv2.CAP_PROP_FRAME_WIDTH ,width) # set size  -> check size
cam.set(cv2.CAP_PROP_FRAME_HEIGHT,height)
##cam.set(cv2.CAP_PROP_FPS, 28)
W = int(cam.get(cv2.CAP_PROP_FRAME_WIDTH))
H = int(cam.get(cv2.CAP_PROP_FRAME_HEIGHT))
if int((W/H)*1000) != int((width/height)*1000):
	print("Camera must support 16:9 aspect ratio:", W,H)
	sys.exit(1)

## fake webcam
if v4l2 :
	fake = pyfakewebcam.FakeWebcam('/dev/video20', width, height)

picmode=False
outimg=None
loopadd=0
while True:
	stat,img = cam.read()
	if stat is False:
		cam.set(cv2.CAP_PROP_POS_FRAMES, 0)
		continue
	###
	if picmode :
		### PIC MODE 
		loopadd=loopadd+1
		for i in range(30):
			theta=math.radians(i*12)
			x=math.cos(theta)
			y=math.sin(theta)
			centerX= int(W/2)
			centerY= int(H/2)
			idx=(i+(int(loopadd*0.8)))%len(cl)
			c=(cl[idx],cl[idx],cl[idx])
			cv2.line(outimg,
					 (int(50*x)+centerX, int(50*y)+centerY),
					 (int(100*x)+centerX, int(100*y)++centerY),
					 c, thickness=10, lineType=cv2.LINE_4)

		cv2.imshow('Cheating Webcam',outimg)
		fakeimg=outimg
	else:
		cv2.imshow('Cheating Webcam', img)
		fakeimg=img
		
	###
	if v4l2 :
		frame = cv2.cvtColor(fakeimg,cv2.COLOR_BGR2RGB)
		resizedFrame = cv2.resize(frame, (width,height))
		fake.schedule_frame(resizedFrame)

	##
	k = cv2.waitKey(1)
	if k & 0xFF == ord('q'): # -> Finish 
		break
	elif k & 0xFF == ord('p'): #-> Pose
		picmode=True
		outimg=img
		loopadd=0
	elif k & 0xFF == ord('r'): #-> Reset
		## reset
		picmode=False
		outimg=None

cv2.destroyAllWindows()
