import datetime
import multiprocessing as mp
import imutils
import cv2
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

class videoStream:
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
	
	while True:
	
		frame = args[0]
		lowerBound = args[1]
		upperBound = args[2]
		gray = args[3]
	
		if not gray:
			#blurred = cv2.GaussianBlur(frame, (11, 11), 0)
			hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
		 
			mask = cv2.inRange(hsv, lowerBound, upperBound)
			mask = cv2.erode(mask, None, iterations=2)
			mask = cv2.dilate(mask, None, iterations=2)
			#print("Processed image")
			#return mask
			mask.put

		else:
			ret,mask = cv2.threshold(frame, lowerBound, upperBound ,cv2.THRESH_BINARY)
			mask = cv2.erode(mask, None, iterations=2)
			mask = cv2.dilate(mask, None, iterations=2)
			#print("Processed image")
			return mask

def main():
	
	manager = mp.Manager()
	frameQueue = manager.Queue()
	
	
	
fps = FPS().start()
vs = videoStream().start()
