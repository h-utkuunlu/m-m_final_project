from __future__ import print_function
from threading import Thread
from multiprocessing import Pool, Process
import numpy as np
import datetime
import imutils
import cv2
#from time import sleep
import serial
import os

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
	def __init__(self, src = -1):

		self.stream = cv2.VideoCapture(src)
		(self.grabbed, self.frame) = self.stream.read()

		self.stopped = False
		
	def start(self):
		self.p = Process(target=self.update, args=())
		self.p.start()
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
		self.p.terminate()

def imageProcess(args):
	
	print('Running the function')
	frame = args[0]
	colorLower = args[1]
	colorUpper = args[2]
	gray = args[3]
	print('start processing')
	
	
	if not gray:
		#blurred = cv2.GaussianBlur(frame, (11, 11), 0)
		hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
	 
		mask = cv2.inRange(hsv, colorLower, colorUpper)
		mask = cv2.erode(mask, None, iterations=2)
		mask = cv2.dilate(mask, None, iterations=2)
		print("Processed image")
		return mask

	else:
		ret,mask = cv2.threshold(frame, 200, 255,cv2.THRESH_BINARY)
		mask = cv2.erode(mask, None, iterations=2)
		mask = cv2.dilate(mask, None, iterations=2)
		print("Processed image")
		return mask

def setArmState(mask, arm):
	
	state_list = [['0', '1'], ['2', '3']][arm]
	
	cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
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
				state = state_list[0].encode()
				#ser.write(state)
				#cv2.circle(bg, center, 3, (255, 0, 255), -1)
			else:
				state = state_list[0].encode()
				#ser.write(state)

	else:
		state = "0".encode()
		#ser.write(state)

input_file = open("images/black.txt")
set_on = set()

for line in input_file:
    
    coordinate = line.strip().split(",")
    for i in range(2):
        coordinate[i] = int(coordinate[i])
    point = (coordinate[0], coordinate[1])
    set_on.add(point)

#print(len(set_on))

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
cp = None
state = '0'.encode()

#ser = serial.Serial('/dev/ttyACM0', 57600)


print("[INFO] sampling THREADED frames from webcam...")
vs = WebcamVideoStream().start()
fps = FPS().start()
bg = cv2.imread("images/bg.png")
cv2.imshow("Frame", bg)

if __name__ == '__main__':

	while True:
		
		masks = []
		print('Start')
		frame = vs.read()
		print('Read')
		p = Pool()
		print('created pool')
		masks = p.map(imageProcess, [[frame, color1Lower, color1Upper, False], [frame, color2Lower, color2Upper, False], [frame, color3Lower, color3Upper, True]])
		print('processed masks')
		p.close()
		print('close')
		p.join()
		print('join')
		
		setArmState(masks[0], 0)
		setArmState(masks[1], 1)
	
		'''
		cnts = cv2.findContours(masks[2].copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
		center = None
	
		if len(cnts) > 0:
			for c in cnts:
			#c = max(cnts, key=cv2.contourArea)
				((x, y), radius) = cv2.minEnclosingCircle(c)
				M = cv2.moments(c)
				center = (int(M["m10"] / M["m00"])*2, int(M["m01"] / M["m00"])*2)
		
				if radius > 2:
		
					cv2.circle(bg, center, 2, (255, 255, 255), -1)
		'''
		
		key = cv2.waitKey(1) & 0xFF
		#cv2.imshow("purple", masks[0])
		#cv2.imshow("red", masks[1])
		#cv2.imshow("display", mask[2])
		if key == ord("q"):
			break
		
		if key == ord("c"):
			bg = cv2.imread("images/bg.png")
		fps.update()

		#if fps.numFrames > 10000:
		#	break
		
		print("I am done with one cycle")

fps.stop()
print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

cv2.destroyAllWindows()
vs.stop()


