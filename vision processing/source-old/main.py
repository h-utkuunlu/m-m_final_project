from __future__ import print_function
from threading import Thread
import numpy as np
import datetime
import imutils
import cv2
#from time import sleep
import serial

class FPS:
	def __init__(self):

		self._start = None
		self._end = None
		self.numFrames = 0
 
	def start(self):

		self._start = datetime.datetime.now()
		return self
 
	def stop(self):

		self._end = datetime.datetime.now()
 
	def update(self):

		self.numFrames += 1
 
	def elapsed(self):

		return (self._end - self._start).total_seconds()
 
	def fps(self):

		return self.numFrames / self.elapsed()

class WebcamVideoStream:
	def __init__(self, src=1):

		self.stream = cv2.VideoCapture(src)
		(self.grabbed, self.frame) = self.stream.read()

		self.stopped = False
		
	def start(self):
		Thread(target=self.update, args=()).start()
		return self
 
	def update(self):
		while True:
			if self.stopped:
				return
 
			(self.grabbed, self.frame) = self.stream.read()
 
	def read(self):
		return self.frame
 
	def stop(self):
		self.stopped = True

def imageProcess(frame, colorLower, colorUpper):
	
	#blurred = cv2.GaussianBlur(frame, (11, 11), 0)
	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
 
	mask = cv2.inRange(hsv, colorLower, colorUpper)
	mask = cv2.erode(mask, None, iterations=2)
	mask = cv2.dilate(mask, None, iterations=2)
	return mask

input_file = open("images/black.txt")
set_on = set()

for line in input_file:
    
    coordinate = line.strip().split(",")
    for i in range(2):
        coordinate[i] = int(coordinate[i])
    point = (coordinate[0], coordinate[1])
    set_on.add(point)

print(len(set_on))


#HSV

#PURPLE
color1Lower = (120, 50, 50)
color1Upper = (160, 255, 255)

#RED
color2Lower = (0, 50, 100)
color2Upper = (10, 255, 255)


#white
color3Lower = (0, 0, 200)
color3Upper = (0, 0, 255)

"""

color2Lower = (10, 240, 240)
color2Upper = (11, 255, 255)



#BGR

color1Lower = (100, 30, 20)
color1Upper = (120, 50, 50)

color2Lower = (10, 240, 240)
color2Upper = (11, 255, 255)

"""
counter = 0
(dX, dY) = (0, 0)
direction = ""
cp = None
state = '0'.encode()

ser = serial.Serial('/dev/ttyACM0', 57600)


print("[INFO] sampling THREADED frames from webcam...")
vs = WebcamVideoStream(src=1).start()
fps = FPS().start()
bg = cv2.imread("images/bg.png")
#cv2.imshow("Frame", bg)

while True:
	
	frame = vs.read()
	
	frame = imutils.resize(frame, width=600)
	mask1 = imageProcess(frame, color1Lower, color1Upper)
	mask2 = imageProcess(frame, color2Lower, color2Upper)
	mask3 = imageProcess(frame, color3Lower, color3Upper)
	
	cnts = cv2.findContours(mask1.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
	center = None
	
	if len(cnts) > 0:

		c = max(cnts, key=cv2.contourArea)
		((x, y), radius) = cv2.minEnclosingCircle(c)
		M = cv2.moments(c)
		center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
		

		if radius > 2:

			#cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 1)
			#cv2.imshow("Frame", frame)
			
			if center in set_on:
				state = "1".encode()
				ser.write(state)
				cv2.circle(bg, center, 3, (255, 0, 255), -1)
			else:
				state = "0".encode()
				ser.write(state)
	
	else:
		state = "0".encode()
		ser.write(state)
	
	cnts = cv2.findContours(mask2.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
	center = None
	
	if len(cnts) > 0:

		c = max(cnts, key=cv2.contourArea)
		((x, y), radius) = cv2.minEnclosingCircle(c)
		M = cv2.moments(c)
		center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
		

		if radius > 2:

			#cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 1)
			#cv2.imshow("Frame", frame)
			
			if center in set_on:
				state = "3".encode()
				ser.write(state)
				cv2.circle(bg, center, 3, (0, 0, 255), -1)
			else:
				state = "2".encode()
				ser.write(state)
	
	else:
		state = "2".encode()
		ser.write(state)
	
	
	
	
	key = cv2.waitKey(1) & 0xFF
	cv2.imshow("purpe", mask1)
	cv2.imshow("red", mask2)
	cv2.imshow("Both", bg)
	if key == ord("q"):
		break
		
	if key == ord("c"):
		bg = cv2.imread("images/bg.png")
	fps.update()

	#if fps.numFrames > 10000:
	#	break
		

fps.stop()
print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

cv2.destroyAllWindows()
vs.stop()


