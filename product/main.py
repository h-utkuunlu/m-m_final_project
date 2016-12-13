from __future__ import print_function
from threading import Thread
from multiprocessing import Pool, Process
import numpy as np
import datetime
import imutils
import cv2
from time import sleep
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
	def __init__(self, src = -1):

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

def image_process(frame, colorLower, colorUpper, gray = False):
	
	
	if not gray:
		#blurred = cv2.GaussianBlur(frame, (11, 11), 0)
		#hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
	 
		mask = cv2.inRange(frame, colorLower, colorUpper)
		mask = cv2.erode(mask, None, iterations=2)
		mask = cv2.dilate(mask, None, iterations=2)

	else:
	
		#bw = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
		mask = cv2.inRange(frame, colorLower, colorUpper)
		#ret,mask = cv2.threshold(frame, 200, 255,cv2.THRESH_BINARY)
		mask = cv2.erode(mask, None)
		mask = cv2.dilate(mask, None, iterations=2)
		
		#
		
	return mask

def set_arm_state(mask, arm):
	state_list = [['1'.encode(), '0'.encode()], ['3'.encode(), '2'.encode()]][arm]
	
	cnts = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
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
				ser.write(state_list[0])
				#cv2.circle(bg, center, 3, (255, 0, 255), -1)
			else:
				ser.write(state_list[1])
	else:
		ser.write(state_list[1])

def update_screen(mask):

	cnts = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
	#cnts, hierarchy = cv2.findContours(display_mask.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	center = None
	
	if len(cnts) > 0:
		for c in cnts:
		#c = max(cnts, key=cv2.contourArea)
			((x, y), radius) = cv2.minEnclosingCircle(c)
			M = cv2.moments(c)
			center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
			
			cv2.circle(bg, center, 3, (255, 255, 255), -1)
			
			#if radius > 2:
				#cv2.circle(bg, (int(x), int(y)), int(radius), (0, 255, 255), 1)
	
	cv2.imshow("Image", bg)
	

input_file = open("images/black.txt")
set_on = set()

for line in input_file:
    
    coordinate = line.strip().split(",")
    for i in range(2):
        coordinate[i] = int(coordinate[i])
    point = (coordinate[0], coordinate[1])
    set_on.add(point)

#PURPLE - HSV
color1Lower = np.array([80, 50, 50], dtype = np.uint8)
color1Upper = np.array([180, 255, 255], dtype = np.uint8)

#YELLOW - HSV
color2Lower = np.array([15, 50, 50], dtype = np.uint8)
color2Upper = np.array([80, 255, 255], dtype = np.uint8)

#WHITE - RGB
#color3Lower = (100, 0, 0)
#color3Upper = (180, 50, 255)

color3Lower = np.array([0,0,180], dtype=np.uint8)
color3Upper = np.array([0,0,255], dtype=np.uint8)

ser = serial.Serial('/dev/ttyACM0', 57600)

ser.write('0'.encode())
sleep(0.5)
ser.write('2'.encode())

print("[INFO] sampling THREADED frames from webcam...")
vs = WebcamVideoStream().start()
fps = FPS().start()
bg = cv2.imread("images/bg.png")
#cv2.imshow("Frame", bg)

while True:
	
	frame = vs.read()
	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
	#frame = imutils.resize(frame, width=600)
	
	mask1 = image_process(hsv, color1Lower, color1Upper)
	mask2 = image_process(hsv, color2Lower, color2Upper)
	display_mask = image_process(hsv, color3Lower, color3Upper, True)
	
	#cv2.imshow('Purple', mask1)
	#cv2.imshow('Yellow', mask2)
	#cv2.imshow('Display', display_mask)
	
	set_arm_state(mask1, 0) # Purple
	set_arm_state(mask2, 1) # Yellow
	
	#ser.write('1'.encode())
	#ser.write('3'.encode())
	
	update_screen(display_mask)
	
	key = cv2.waitKey(1) & 0xFF
		
	if key == ord("q"):
		break
		
	if key == ord("c"):
		bg = cv2.imread("images/bg.png")
	fps.update()

	if key == ord("f"):
		fps.stop()
		print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
		print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

fps.stop()
print("[INFO] total elasped time: {:.2f}".format(fps.elapsed()))
print("[INFO] overall approx. FPS: {:.2f}".format(fps.fps()))

cv2.destroyAllWindows()
vs.stop()
