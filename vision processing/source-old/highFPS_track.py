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
		# store the start time, end time, and total number of frames
		# that were examined between the start and end intervals
		self._start = None
		self._end = None
		self.numFrames = 0
 
	def start(self):
		# start the timer
		self._start = datetime.datetime.now()
		return self
 
	def stop(self):
		# stop the timer
		self._end = datetime.datetime.now()
 
	def update(self):
		# increment the total number of frames examined during the
		# start and end intervals
		self.numFrames += 1
 
	def elapsed(self):
		# return the total number of seconds between the start and
		# end interval
		return (self._end - self._start).total_seconds()
 
	def fps(self):
		# compute the (approximate) frames per second
		return self.numFrames / self.elapsed()

class WebcamVideoStream:
	def __init__(self, src=1):
		# initialize the video camera stream and read the first frame
		# from the stream
		self.stream = cv2.VideoCapture(src)
		(self.grabbed, self.frame) = self.stream.read()
 
		# initialize the variable used to indicate if the thread should
		# be stopped
		self.stopped = False
		
	def start(self):
		# start the thread to read frames from the video stream
		Thread(target=self.update, args=()).start()
		return self
 
	def update(self):
		# keep looping infinitely until the thread is stopped
		while True:
			# if the thread indicator variable is set, stop the thread
			if self.stopped:
				return
 
			# otherwise, read the next frame from the stream
			(self.grabbed, self.frame) = self.stream.read()
 
	def read(self):
		# return the frame most recently read
		return self.frame
 
	def stop(self):
		# indicate that the thread should be stopped
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

# define the lower and upper boundaries of the "green"
# ball in the HSV color space
colorLower = (90, 30, 30)
colorUpper = (130, 245, 245)
 
# initialize the list of tracked points, the frame counter,
# and the coordinate deltas
counter = 0
(dX, dY) = (0, 0)
direction = ""
cp = None
state = '0'.encode()

ser = serial.Serial('/dev/ttyACM0', 57600)


# created a *threaded* video stream, allow the camera sensor to warmup,
# and start the FPS counter
print("[INFO] sampling THREADED frames from webcam...")
vs = WebcamVideoStream(src=1).start()
fps = FPS().start()
bg = cv2.imread("images/bg.png")
cv2.imshow("Frame", bg)

# loop over some frames...this time using the threaded stream
while True:
	
	#sleep(0.01)
	
	frame = vs.read()
	
	# resize the frame, blur it, and convert it to the HSV
	# color space
	frame = imutils.resize(frame, width=600)
	mask = imageProcess(frame, colorLower, colorUpper)
	
	
	
	# find contours in the mask and initialize the current
	# (x, y) center of the ball
	
	cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
	center = None
	
	# only proceed if at least one contour was found
		
	if len(cnts) > 0:
		# find the largest contour in the mask, then use
		# it to compute the minimum enclosing circle and
		# centroid
		
		c = max(cnts, key=cv2.contourArea)
		((x, y), radius) = cv2.minEnclosingCircle(c)
		M = cv2.moments(c)
		center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
		
 		
		# only proceed if the radius meets a minimum size
		if radius > 2:
			# draw the circle and centroid on the frame,
			# then update the list of tracked points
			#cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 1)
			#cv2.imshow("Frame", frame)
			
			if center in set_on:
				state = "1".encode()
				ser.write(state)
				cv2.circle(bg, center, 3, (0, 0, 255), -1)
			else:
				state = "0".encode()
				ser.write(state)
	# show the frame to our screen and increment the frame counter
	
	
	#key = cv2.waitKey(1) & 0xFF
	#cv2.imshow("Frame", bg)
	# if the 'q' key is pressed, stop the loop
	#if key == ord("q"):
	#	break
	fps.update()
	# update the FPS counter
	
	if fps.numFrames > 10000:
		break
		
# stop the timer and display FPS information
fps.stop()
print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))


# do a bit of cleanup
cv2.destroyAllWindows()
vs.stop()


