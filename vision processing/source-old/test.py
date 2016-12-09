import numpy as np
import cv2
"""
green = np.uint8([[[0, 255, 0 ]]])
hsv_green = cv2.cvtColor(green,cv2.COLOR_BGR2HSV)
print(hsv_green)




balls = cv2.imread("color_ball.jpg", -1)

#cv2.imshow('image',balls)

hsv = cv2.cvtColor(balls , cv2.COLOR_BGR2HSV)

#cv2.imshow('image',hsv)

lower_blue = np.array([100, 100, 100])#np.array([143, 48, 53])
upper_blue = np.array([120, 255, 255])

mask = cv2.inRange(hsv, lower_blue, upper_blue)
res = cv2.bitwise_and(balls, balls, mask = mask)

cv2.imshow('mask', res)



cv2.waitKey(0)
cv2.destroyAllWindows()


"""

cap = cv2.VideoCapture(1)

cap.set(10,0)


while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    cv2.imshow('res', frame)
    
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()


