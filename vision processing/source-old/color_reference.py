import numpy as np
import cv2
import imutils

def imageProcess(frame, colorLower, colorUpper):
	
	#blurred = cv2.GaussianBlur(frame, (11, 11), 0)
	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
 
	mask = cv2.inRange(hsv, colorLower, colorUpper)
	mask = cv2.erode(mask, None, iterations=2)
	mask = cv2.dilate(mask, None, iterations=2)
	return mask

#HSV

#Blue

color1Lower = (110, 50, 20)
color1Upper = (130, 180, 180)

#Red

#Not as good

color2Lower = (0, 50, 100)
color2Upper = (20, 255, 255)

#Green

color3Lower = (60, 50, 20)
color3Upper = (100, 255, 255)

#frame = cv2.imread('images/color_check2.jpg',1)


cap = cv2.VideoCapture(1)

cap.set(10,0)


while True:
    # Capture frame-by-frame
	ret, frame = cap.read()

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

			cv2.circle(frame, (int(x), int(y)), int(radius), (255, 0, 0), 1)
			#cv2.imshow("Frame", frame)
		
			cv2.circle(frame, center, 2, (255, 255, 255), -1)


	cnts = cv2.findContours(mask2.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
	center = None

	if len(cnts) > 0:

		c = max(cnts, key=cv2.contourArea)
		((x, y), radius) = cv2.minEnclosingCircle(c)
		M = cv2.moments(c)
		center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
	

		if radius > 2:

			cv2.circle(frame, (int(x), int(y)), int(radius), (0, 0, 255), 1)
			#cv2.imshow("Frame", frame)
		
			cv2.circle(frame, center, 2, (255, 255, 255), -1)

	cnts = cv2.findContours(mask3.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
	center = None

	if len(cnts) > 0:

		c = max(cnts, key=cv2.contourArea)
		((x, y), radius) = cv2.minEnclosingCircle(c)
		M = cv2.moments(c)
		center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
	

		if radius > 2:

			cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 0), 1)
			#cv2.imshow("Frame", frame)
		
			cv2.circle(frame, center, 2, (255, 255, 255), -1)
	
	cv2.imshow("Frame", frame)
	
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

	

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()

	


"""

cv2.imshow('image',frame)
#cv2.imshow("Blue", mask1)
#cv2.imshow("red", mask2)
#cv2.imshow("green", mask3)
cv2.waitKey(0)
cv2.destroyAllWindows()

"""


