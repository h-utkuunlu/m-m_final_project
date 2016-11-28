import numpy as np
import cv2

color = np.uint8([[[125, 31, 23 ]]])
hsv = cv2.cvtColor(color,cv2.COLOR_BGR2HSV)
print(hsv)
