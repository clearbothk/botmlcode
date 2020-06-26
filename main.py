from detector import yolo
import cv2

"""
Sample code importing the detector module
"""
print("[INFO] accessing video stream...")
vs = cv2.VideoCapture(0)
detector = yolo.Detector("model", use_gpu=True, weights_file="clearbot_26_06_20.weights")
while True:
	(grabbed, frame) = vs.read()
	if not grabbed:
		break
	result = detector.detect(frame)
	print(result)