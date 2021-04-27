from scipy.spatial import distance as dist
from imutils import face_utils
import win32api, win32con
import numpy as np
import imutils
import time
import dlib
import cv2
import matplotlib.pyplot as plt

def eye_aspect_ratio(eye):
	# compute the euclidean distances between the two sets of
	# vertical eye landmarks (x, y)-coordinates
	A = dist.euclidean(eye[1], eye[5])
	B = dist.euclidean(eye[2], eye[4])
	# compute the euclidean distance between the horizontal
	# eye landmark (x, y)-coordinates
	C = dist.euclidean(eye[0], eye[3])
	# compute the eye aspect ratio
	ear = (A + B) / (2.0 * C)
	# return the eye aspect ratio
	return ear

def moving_average(x, w):
    return np.convolve(x, np.ones(w), 'valid') / w

MOVE_AVERAGE = 10
Blink_average = 6

left_array = np.zeros([400])
right_array = np.zeros([400])

left_average = np.zeros([Blink_average])
right_average = np.zeros([Blink_average])

leftEAR = 0
rightEAR = 0

# define two constants, one for the eye aspect ratio to indicate
# blink and then a second constant for the number of consecutive
# frames the eye must be below the threshold
EYE_AR_THRESH = 0.26
EYE_AR_CONSEC_FRAMES = 2
# initialize the frame counters and the total number of blinks
COUNTER_LEFT = 0
COUNTER_RIGHT = 0
TOTAL_LEFT = 0
TOTAL_RIGHT = 0

print("[INFO] loading facial landmark predictor...")
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')

# grab the indexes of the facial landmarks for the left and
# right eye, respectively
(lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
(rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]

captura = cv2.VideoCapture(0)

# name = input('Digite seu nome: ') # trocar no final do dev
name = "DEBUG"
fileName = name + '_labels' + '.csv'

f = open(fileName, 'w')
f.write('blinks\n')

while True:
	ret, frame = captura.read()
	
	frame = imutils.resize(frame, width=850)
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

	rects = detector(gray, 0)

	# loop over the face detections
	for rect in rects:
		# determine the facial landmarks for the face region, then
		# convert the facial landmark (x, y)-coordinates to a NumPy
		# array
		shape = predictor(gray, rect)
		shape = face_utils.shape_to_np(shape)
		# extract the left and right eye coordinates, then use the
		# coordinates to compute the eye aspect ratio for both eyes
		leftEye = shape[lStart:lEnd]
		rightEye = shape[rStart:rEnd]
		leftEAR = eye_aspect_ratio(leftEye)
		rightEAR = eye_aspect_ratio(rightEye)

		left_average = np.roll(left_average, 1)
		left_average[0] = leftEAR
		leftEAR = left_average.sum()/Blink_average

		right_average = np.roll(right_average, 1)
		right_average[0] = rightEAR
		rightEAR = right_average.sum()/Blink_average
  
		# average the eye aspect ratio together for both eyes

		leftEyeHull = cv2.convexHull(leftEye)
		rightEyeHull = cv2.convexHull(rightEye)
		cv2.drawContours(frame, [leftEyeHull], -1, (0, 255, 0), 1)
		cv2.drawContours(frame, [rightEyeHull], -1, (0, 255, 0), 1)

		if leftEAR < EYE_AR_THRESH:
			COUNTER_LEFT += 1
		else:
			if COUNTER_LEFT >= EYE_AR_CONSEC_FRAMES:
				TOTAL_LEFT += 1
				f.write(str(time.time()) + ',3\n')
				win32api.keybd_event(0x20,0,0,0) # holds the "F" key down
				time.sleep(0.1) # waits 2 seconds
				win32api.keybd_event(0x20,0,win32con.KEYEVENTF_KEYUP,0)
			COUNTER_LEFT = 0
		if rightEAR < EYE_AR_THRESH:
			COUNTER_RIGHT += 1
		else:
			if COUNTER_RIGHT >= EYE_AR_CONSEC_FRAMES:
				TOTAL_RIGHT += 1
				f.write(str(time.time()) + ',2\n')
			COUNTER_RIGHT = 0

		cv2.putText(frame, "Blinks Left: {}".format(TOTAL_LEFT), (10, 30),
		cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)
		cv2.putText(frame, "Blinks Right: {}".format(TOTAL_RIGHT), (10, 80),
		cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)
		cv2.putText(frame, "Left EAR: {:.2f}".format(leftEAR), (10, 590),
		cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
		cv2.putText(frame, "Right EAR: {:.2f}".format(rightEAR), (10, 500),
		cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)

	left_array = np.roll(left_array, 1)
	right_array = np.roll(right_array, 1)
	left_array[0] = leftEAR
	right_array[0] = rightEAR

	smooth_left = moving_average(left_array, MOVE_AVERAGE)
	smooth_right = moving_average(right_array, MOVE_AVERAGE)

	cv2.line(frame, (200, 550-int(EYE_AR_THRESH*300)), (850, 550-int(EYE_AR_THRESH*300)), (255, 255, 0))
	cv2.line(frame, (200, 635-int(EYE_AR_THRESH*300)), (850, 635-int(EYE_AR_THRESH*300)), (255, 255, 0))

	for i, y in enumerate(smooth_right):
		if y > 0:
			cv2.circle(frame, (200 + 4*i, 550-int(300*y)), 2, (255, 0, 0), -1)
	for i, y in enumerate(smooth_left):
		if y > 0:
			cv2.circle(frame, (200 + 4*i, 635-int(300*y)), 2, (0, 0, 255), -1)

	cv2.imshow("Video", frame)
 
	k = cv2.waitKey(30) & 0xff
	if k == 27:
		break
 
captura.release()
cv2.destroyAllWindows()

f.close()