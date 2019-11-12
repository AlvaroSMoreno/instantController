import pyautogui
import cv2
import numpy as np 
WIDTH, HEIGHT = pyautogui.size()
offset, cnt, max_area = 10, 0, 0
cap = cv2.VideoCapture(0)
if not cap.isOpened():
	raise Exception("Could not open video device")
cap.set(cv2.CAP_PROP_FRAME_WIDTH, WIDTH)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, HEIGHT)
posX, posY, oldX, oldY = WIDTH/2,HEIGHT/2, WIDTH/2,HEIGHT/2
while True:
	ret, frame = cap.read()
	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
	curr_x, curr_y = pyautogui.position()
	greenLower = np.array([29, 86, 6])
	greenUpper = np.array([64, 255, 255])
	green_mask = cv2.inRange(hsv, greenLower, greenUpper)
	contours, hierarchy = cv2.findContours(green_mask, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
	max_area = 0
	for contour in contours: 		
		area = cv2.contourArea(contour)
		if(area > 800):
			x,y,w,h = cv2.boundingRect(contour)
			if area > max_area:
				max_area = area
				posX, posY = (((x+w/2-0)*(0-WIDTH))/(WIDTH-0))+WIDTH, y+h
			frame = cv2.rectangle(frame, (x,y),(x+w,y+h),(0,0,255),2)
			break
	if max_area != 0:
		if oldX+offset>posX and oldX-offset<posX and oldY+offset>posY and oldY-offset<posY:
			cnt += 1
		else:
			cnt = 0
			pyautogui.moveTo(posX, posY)
		if cnt > 35:
			pyautogui.click()
			#print('click!')
			cnt = 0
		oldX, oldY = posX, posY
	#cv2.imshow("test", frame)
	k = cv2.waitKey(5) & 0XFF 
	if k == 27:
		break
cv2.destroyAllWindows()
cap.release()